# Short Version
Begin by ensuring that Docker is installed on the engineers Linux/OSX/Windows laptop, then run:
``` bash
docker run -d -p 80:8080 -p 50000:50000 kenerwin88/cb-challenge
```
After a minute or so, a Jenkins server should become available on port 80.  Open a web browser and visit http://localhost.  Optionally, in the event that Docker is NOT available, visit [http://35.161.22.102](http://35.161.22.102) (This is a Jenkins server temporarily available on AWS for this demo).  Once Jenkins comes up, you should see something like this:

![step 1](https://raw.githubusercontent.com/kenerwin88/cb-jenkins/master/images/1.png)

If you would like to just launch a basic CoreOS AWS instance with a webserver, click the "Launch Webserver" Jenkins job.  If you would like to specify a public key to be added to the instance, choose "Launch Webserver with-PublicKey" instead.

![step 2](https://raw.githubusercontent.com/kenerwin88/cb-jenkins/master/images/2.png)

Next, click "Build with Parameters".  You should be redirected to a screen that looks like this:

![step 3](https://raw.githubusercontent.com/kenerwin88/cb-jenkins/master/images/3.png)

Type in your AWS access ID, AWS secret access key, select a region, AMI, and type in the name of your ssh key, then hit "Build".  If you chose to include a public key, you'll also want to select that as well (A sample public and private key are provided within the repo!).

**NOTE: Please make sure that the AWS access ID & secret key have adequate permissions for lauching a new instance as well as creating a new security group!**

Within a few minutes, a new instance named "Coinbase-WEB01-Test" should come up in the AWS region that you specified.  At this point, you should be able to open up a web browser, go to http:// followed by the IP of the new instance, and see the webserver return a webpage that looks like this.

![step 4](https://raw.githubusercontent.com/kenerwin88/cb-jenkins/master/images/4.png)

And that's it for the short version!

# Long Version / Notes
First, if you would rather test out the demo without using Docker or Jenkins, you can also run the [newInstance.py](https://raw.githubusercontent.com/kenerwin88/cb-jenkins/master/scripts/newInstance.py) or [newInstanceWithPubKey.py](https://raw.githubusercontent.com/kenerwin88/cb-jenkins/master/scripts/newInstanceWithPubKey.py) Python scripts directly, just be sure to pass in 5 arguments, the AWS Access ID, Secret Access Key, AWS Region, CoreOS AMI Id, and Keypair name in that order.

Alright, for the choices/techniques.  I chose to use a Docker container to house the whole project for two reasons, one, to make it very easy to get it running quickly without having to worry too much about environment diferences, and two, because from what I've read, Coinbase heavily uses Containers, so I thought it'd fit right in :).

For Jenkins, I chose to use it in order to make it as easy as possible for a non-developer/engineer to kick off a new webserver.  In real life, I wouldn't have the engineer set up Jenkins (Or some other CI platform), it would have already been setup, along with having actual authentication, role based access, etc.  Also, the build/deploy process would also include automated testing, an actual CI pipeline and a bunch of other things in a real life scenario, and it may not even include Jenkins depending on the technology being used at Coinbase.

If you'd like to build the Jenkins Docker container from scratch, you should be able to clone my repository here: [https://github.com/kenerwin88/cb-jenkins](https://github.com/kenerwin88/cb-jenkins), then run:

``` bash
docker build -t kenerwin88/cb-challenge .
```
This Jenkins VM is then configured automatically using Jenkins Job Builder (parses YAML files to build the Jobs).  For the actual launching of the servers, the two Python scripts use Boto3, which is a pretty nice little library for managing AWS resources, although Boto2 has quite a bit more examples at the moment.  In real life, I'd also do some checking to ensure that the instance does actually come up, as well as automated testing, using Selenium, CasperJS, or something like that.

The Python script also takes care of creating an AWS security group, with port 80 and 22 open to the instance.  The CoreOS instance is then configured by providing some Userdata.  This Userdata is what takes care of launching the web server, which is actually another Docker container, which you can view the source of here: [https://github.com/kenerwin88/cb-web](https://github.com/kenerwin88/cb-web).  I ended up pushing it to DockerHub (as well as the Jenkins container), to make it super easy to pull both of them down.

Here's the URLs to the containers on DockerHub.com:
- [https://hub.docker.com/r/kenerwin88/cbweb/](https://hub.docker.com/r/kenerwin88/cbweb/)
- [https://hub.docker.com/r/kenerwin88/cb-challenge/](https://hub.docker.com/r/kenerwin88/cb-challenge/)

I did want to add a job to take care of autoscaling, unfortunately I've been much busier today than I thought I would be.  Also, I'd probably use ECS or at least consider it for production, and I'd also want to set up etcd or consul for service discovery.  Plus it would be nice to add some monitoring as well, and to clean up the code/add error handling.  Overall it was a fun challenge and thank you so much for taking the time to read this!

:) - Ken
