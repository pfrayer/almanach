# Logs

## Generate fake logs

If you need to generate fake logs, use [mingrammer/flog](https://github.com/mingrammer/flog):

```shell
# 1048576 is the size of logs to generate (in bytes)
$ docker run -it --rm mingrammer/flog -b 1048576 > 1_mega.log

# If you want to continuously generate logs (without a file size)
# for instance generate fake Apache logs
# with one new log each 2sec
$ docker run -it --rm mingrammer/flog -f apache_combined -t stdout -n 2 -l
```
It supports several logs format for the output file, more details on the project's [README](https://github.com/mingrammer/flog/blob/master/README.md).
