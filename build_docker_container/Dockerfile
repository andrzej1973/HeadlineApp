FROM ruby:2.2 

RUN apt-get update && gem update --system && gem install bundler 
RUN git init
RUN git remote add origin https://github.com/Distelli/sinatra-app
RUN git fetch
RUN git checkout -t origin/master
RUN bundle install 
EXPOSE 8080 
CMD ["rackup", "-p", "8080", "--host", "127.0.0.1"]