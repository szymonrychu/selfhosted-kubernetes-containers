module.exports = {
  "dryRun": null,
  "username": "szymonrichert.pl bot",
  "gitAuthor": "szymonrichert.pl bot <bot@szymonrichert.pl>",
  "onboarding": false,
  "platform": "github",
  "repositories": ["szymonrychu/containers"],
  "customManagers": [
    {
      "customType": "regex",
      "fileMatch": ["(^|/)Chart\\.yaml$"],
      "matchStrings": [
        "#\\s?renovate: image=(?<depName>.*?)\\s?ARG\\s[\\w+\\_]*\\s?=\\s?\\\"?(?<currentValue>[\\w+\\.\\-]*)"
      ],
      "datasourceTemplate": "docker"
    },
  ],
  "packageRules": [
    {
      "description": "lockFileMaintenance",
      "matchUpdateTypes": [
        "pin",
        "digest",
        "patch",
        "minor",
        "major",
        "lockFileMaintenance"
      ],
      "dependencyDashboardApproval": false,
      "minimumReleaseAge": null
    },
    {
      "matchManagers": ["regex"],
      "postUpgradeTasks": {
        "commands": [
          "version=$(cat {{{parentDir}}}/VERSION | awk '{print $2}')\n            major=$(echo $version | cut -d. -f1)\n            minor=$(echo $version | cut -d. -f2)\n            patch=$(echo $version | cut -d. -f3)\n            minor=$(expr $minor + 1)\n            echo \"Replacing $version with $major.$minor.$patch\"\n            echo \"$major.$minor.$patch\" > {{{parentDir}}}/VERSION\n            cat {{{parentDir}}}/VERSION\n            "
        ],
        "executionMode": "branch"
      }
    }
  ]
};