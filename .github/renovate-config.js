module.exports = {
  "semanticCommits": "enabled",
  "extends": ["config:recommended", ":rebaseStalePrs"],
  "dependencyDashboard": false,
  "dryRun": null,
  "dependencyDashboard": false,
  "suppressNotifications": ["prIgnoreNotification"],
  "commitMessageTopic": "{{depName}}",
  "commitMessageExtra": "to {{newVersion}}",
  "commitMessageSuffix": "",
  "rebaseWhen": "conflicted",
  "prConcurrentLimit": 100,
  "pinDigests": true,
  "automerge": true,
  "username": "szymonrichert.pl bot",
  "gitAuthor": "szymonrichert.pl bot <bot@szymonrichert.pl>",
  "onboarding": false,
  "platform": "github",
  "repositories": ["szymonrychu/containers"],
  "customManagers": [
    {
      "customType": "regex",
      "fileMatch": ["(^|/)Dockerfile$"],
      "matchStrings": [
        "#\\s?renovate: image=(?<depName>.*?)\\s?ARG\\s[\\w+\\_]*\\s?=\\s?\\\"?(?<currentValue>[\\w+\\.\\-]*)"
      ],
      "datasourceTemplate": "docker"
    },
  ],
  "packageRules": [
    {
      "matchManagers": ["regex"],
      "postUpgradeTasks": {
        "commands": [
          "version=$(cat {{{parentDir}}}/VERSION | awk '{print $2}')\n            major=$(echo $version | cut -d. -f1)\n            minor=$(echo $version | cut -d. -f2)\n            patch=$(echo $version | cut -d. -f3)\n            minor=$(expr $minor + 1)\n            echo \"Replacing $version with $major.$minor.$patch\"\n            echo \"$major.$minor.$patch\" > {{{parentDir}}}/VERSION\n            cat {{{parentDir}}}/VERSION\n            "
        ],
        "executionMode": "branch"
      }
    },
    {
      "matchUpdateTypes": ["major"],
      "matchBaseBranches": ["stable"],
      "enabled": false
    }
  ]
};