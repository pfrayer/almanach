# Debian

## Which package for ... ?

```shell
# ps: command not found
$ apt install procps
# netstat: command not found
$ apt install net-tools
```

## List files installed from a given package

```shell
# dpkg-query -L <package_name>
$ dpkg-query -L webp
/.
/usr
/usr/bin
/usr/bin/cwebp
/usr/bin/dwebp
/usr/bin/gif2webp
...
```

## Which package installed a given binary ?

```shell
# dpkg -S <package_name>
$ dpkg -S cwebp
webp: /usr/bin/cwebp
webp: /usr/share/man/man1/cwebp.1.gz
```
