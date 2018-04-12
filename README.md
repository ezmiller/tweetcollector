# Tweetcollector

**TODO: Add setup instructions**

To run from a shell:

`docker-compose run tweetcollector /bin/bash`

To run in the background:

`docker-compose run tweetcollector bash -c './config/setup_aws.sh && ./collect-tweets -q <twitter query> -c <mongo collection name>'`

If running in the background, stop by attaching (`docker attach <container id>`) and then <Ctrl-C>.
