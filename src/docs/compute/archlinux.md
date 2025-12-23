# ArchLinux

## Install an AUR package manually

```shell
# Example: install yay from AUR
$ sudo pacman -S --needed git base-devel
$ git clone https://aur.archlinux.org/yay.git
$ cd yay
$ makepkg -si
```

## `yay` cheatsheet

| Feature | Command |
| ------- | ------- |
| Search (official + AUR) | `yay package_name` |
| Install a package | `yay -S package_name` |
| Upgrade all packages (AUR) | `yay -Syu` |
| Clean cache | `yay -Sc` |
| Remove unused dependencies | `yay -Yc` |
| Remove package & config | `yay -Rns package_name` |
| Install only AUR package | `yay -S package_name --aur` |
| Install only repo package | `yay -S package_name --repo` |
| View package info | `yay -Si package_name` |
| View package file paths | `yay -Ql package_name` |
| Find package owning a file | `yay -Qo /path/to/file` |
| List installed AUR packages | `yay -Qm` |

[Source](https://ehewen.com/en/blog/yay/){target=_blank}
