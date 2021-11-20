./gradlew clean
curl -s "https://get.sdkman.io" | bash
source "/home/vscode/.sdkman/bin/sdkman-init.sh"
sdk install java
sdk install groovy
./src/docs/generateIndex.groovy
./gradlew generateHTML
echo 0