import subprocess
import shlex
import os
import logging
import json
import tempfile
from threading import Thread
import time
from datetime import datetime, timedelta

class CMDError(Exception):
    pass

class CMD():

    def __init__(self, cmd, cwd=None, env={}, shell=False):
        self.__cmd = cmd
        self.__cwd = cwd
        self.__env = env
        self.__shell = shell
        self.__last_stdout_line_N = 0
        self.__last_stderr_line_N = 0
        self.__stdout = ''
        self.__stderr = ''
        self.__rc = -1
    
    @property 
    def stdout(self):
        return self.__stdout
    
    @property 
    def stderr(self):
        return self.__stderr
    
    @property 
    def rc(self):
        return self.__rc

    def __format_output(self, prefix, output, indent=2):
        _indent = ' '*indent
        result = [prefix, ':\n']
        for line in output.split('\n'):
            result.append(f'{_indent}{line}\n')
        return ''.join(result)

    def run(self, timeout=-1, polling_sleep_s=1):
        list(self.run_with_handler(timeout=timeout, polling_sleep_s=polling_sleep_s))

    def run_with_handler(self, timeout=-1, polling_sleep_s=1, handler=None, handler_args=(), handler_kwargs={}):
        _handler = handler or self._handler
        logging.debug('Running command: "{}"'.format(self.__cmd))
        if self.__env:
            logging.debug('  with env\n:{}'.format('\n'.join(["    {}='{}'".format(k, v) for k, v in self.__env.items()])))
        _env = dict(os.environ)
        _env.update(self.__env)
        start_time = time.time()
        timeout_reached = False
        stdout_lines = []
        stderr_lines = []
        _subprocess = subprocess.Popen(shlex.split(self.__cmd), cwd=self.__cwd, env=_env, shell=self.__shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.set_blocking(_subprocess.stdout.fileno(), False)
        os.set_blocking(_subprocess.stderr.fileno(), False)
        while True:
            new_stdout_lines = [l.decode().rstrip() for l in list(_subprocess.stdout)[self.__last_stdout_line_N:]]
            self.__last_stdout_line_N += len(new_stdout_lines)
            stdout_lines.extend(new_stdout_lines)
            self.__stdout = '\n'.join(stdout_lines).rstrip()
            if self.__stdout:
                logging.debug(self.__stdout)

            new_stderr_lines = [l.decode().rstrip() for l in list(_subprocess.stderr)[self.__last_stderr_line_N:]]
            self.__last_stderr_line_N += len(new_stderr_lines)
            stderr_lines.extend(new_stderr_lines)
            self.__stderr = '\n'.join(stderr_lines).rstrip()
            if self.__stderr:
                logging.debug(self.__stderr)

            handler_output = _handler(*handler_args, **handler_kwargs)
            if handler_output:
                yield handler_output

            self.__rc = _subprocess.poll()

            if self.__rc is None:
                time.sleep(polling_sleep_s)
            else:
                break
            
            timeout_reached = timeout > 0 and time.time() - start_time > timeout
            if timeout_reached:
                break
        
        _subprocess.terminate()
        _subprocess.wait()

        _stdout = self.__format_output('stdout', '\n'.join(stdout_lines).rstrip())
        _stderr = self.__format_output('stderr', '\n'.join(stderr_lines).rstrip())

        if timeout_reached:
            raise CMDError(f"Reached timeout {timeout}s for command:\n  '{self.__cmd}'\n{_stdout}\n{_stderr}")

        if self.__rc != 0:
            raise CMDError(f"RC!=0 {self.__rc} for command:\n  '{self.__cmd}'\n{_stdout}\n{_stderr}")
        return 
    
    def _handler(self, *args, **kwargs):
        return None

class FFMpegFileError(Exception):
    pass

class FFMpegFile():
    
    def __init__(self, fpath):
        self.__fpath = fpath
        _cmd = CMD(f'ffprobe -print_format json -show_streams -show_format -pretty -loglevel quiet {self.__fpath}')
        try:
            _cmd.run()
        except CMDError:
            raise FFMpegFileError('Invalid file')
        if _cmd.stderr:
            raise FFMpegFileError('FFMpeg shouldnt return stderr!')
        self._metadata = json.loads(_cmd.stdout)
        self._video_stream_id = -1
        self._audio_stream_id = -1
        if self.is_video:
            for id, stream in enumerate(self._metadata['streams']):
                if self._video_stream_id < 0 and stream['codec_type'] == 'video':
                    self._video_stream_id = id
                elif self._audio_stream_id < 0 and stream['codec_type'] == 'audio':
                    self._audio_stream_id = id
        self.__data_len = 0

    @property
    def is_video(self):
        return self._video_stream_id != -1

    @property
    def resolution(self):
        return (
            self._metadata['streams'][self._video_stream_id]['width'],
            self._metadata['streams'][self._video_stream_id]['height'],
        )
    
    @property
    def is_hevc(self):
        return self.is_video and self._metadata['streams'][0]['codec_name'] == 'hevc'

    @property
    def duration(self):
        try:
            t = datetime.strptime(self._metadata['format']['duration'], "%H:%M:%S.%f")
            return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond).total_seconds()
        except KeyError:
            return -1

    @property
    def streams_n(self):
        return len(self._metadata['streams'])

    @property
    def path(self):
        return self.__fpath

    def __str__(self) -> str:
        return json.dumps(self._metadata, indent=2)

    def _update_handler(self, tmp_name):
        data = ""
        with open(tmp_name, 'r') as f:
            f.seek(self.__data_len)
            data = f.read()
        self.__data_len += len(data)
        if data:
            result = {}
            for detail in [l for l in data.split('\n') if l]:
                k, v = detail.split('=')
                result[k] = v
            result['progress'] = round(1000*float(result['out_time_ms'])/(1000000.0*self.duration))/10.0
            return result
        else:
            return {}

    def convert(self, stats_period=1, out_path=None, output_resolution=None, output_bitrate='10M', threads=1, overwrite=False):
        src_fpath_wo_ext, src_fname_ext = '.'.join(self.__fpath.split('.')[:-1]), self.__fpath.split('.')[-1]
        src_fname_wo_ext = os.path.basename(src_fpath_wo_ext)
        subtitles_fpath = '.'.join([src_fpath_wo_ext, 'srt'])

        if not out_path:
            out_path = os.path.join(os.path.dirname(self.__fpath), f"{src_fname_wo_ext}_tmp.{src_fname_ext}")
        
        if os.path.isfile(out_path):
            if overwrite:
                logging.warning(f"Temporary output file already exists, removing '{out_path}'")
                os.remove(out_path)
            else:
                raise FFMpegFileError('Conversion already happens!')
        
        has_subtitles = os.path.isfile(subtitles_fpath)

        with tempfile.NamedTemporaryFile() as tmp:
            cmd = [
                'ffmpeg',
                f'-i {self.__fpath}',
            ]

            if has_subtitles:
                cmd.extend([
                    f'-i {subtitles_fpath}',
                ])
            
            cmd.extend([
                '-map 0:0',
                '-map 0:1'
            ])
            if has_subtitles:
                cmd.extend([
                    '-map 1:0',
                    '-c:s srt',
                    '-metadata:s:s:0 language=pl',
                ])
            
            scale = ''
            if output_resolution:
                scale = f'scale={output_resolution[0]}:{output_resolution[1]}:flags=lanczos,'
            
            
            cmd.extend([
                f'-progress {tmp.name}',
                f'-stats_period {stats_period}',
                '-c:v libx264',
                '-crf 18',
                f'-vf {scale}format=yuv420p',
                '-c:a copy',
                f'-maxrate {output_bitrate}',
                f'-bufsize {output_bitrate}',
                f'-threads {threads}',
                out_path
            ])

            logging.info(f"Started convert from '{self.__fpath}' to '{out_path}' using {threads} threads")

            _c = CMD(' '.join(cmd))
            yield from _c.run_with_handler(polling_sleep_s=stats_period, handler=self._update_handler, handler_kwargs={
                'tmp_name': tmp.name
            })
        
        os.remove(self.__fpath)
        os.remove(subtitles_fpath)
        os.rename(out_path, self.__fpath)

        
            

