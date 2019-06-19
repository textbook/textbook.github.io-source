FROM debian:stretch

LABEL "com.github.actions.name"="Checkout submodules"
LABEL "com.github.actions.description"="Recursively checks out any submodules in your repo"
LABEL "com.github.actions.icon"="mic"
LABEL "com.github.actions.color"="blue"

RUN apt-get -y update && apt-get -y install git && apt-get clean

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
