#!/bin/bash

cd /var/lib/librum-server/srv


export JWTValidIssuer="${JWT_VALID_ISSUER:-exampleIssuer}"
export JWTKey="${JWT_KEY:-exampleOfALongSecretToken}"
export AdminEmail="${ADMIN_EMAIL:-admin@example.com}"
export AdminPassword="${ADMIN_PASSWORD:-strongPassword123}"
export DBConnectionString="Server=${DB_HOST:-127.0.0.1};port=${DB_PORT:-3306};Database=${DB_NAME:-my_database_name};Uid=${DB_USERNAME:-mysql_user};Pwd=${DB_PASSWORD:-mysql_password};"
export SMTPEndpoint="${SMTP_HOST:-smtp.example.com}"
export SMTPUsername="${SMTP_USERNAME:-mailuser123}"
export SMTPPassword="${SMTP_PASSWORD:-smtpUserPassword123}"
export SMTPMailFrom="${SMTP_MAIL_FROM:-mailuser123@example.com}"
export CleanUrl="${CLEAN_URL:-https://127.0.0.1}"
export OpenAIToken="${OPEN_AI_TOKEN}"
export ASPNETCORE_ENVIRONMENT="Production"
export LIBRUM_SELFHOSTED="true"

dotnet Presentation.dll