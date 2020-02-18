#!/bin/bash

cur_date=$(date +%Y_%m_%d)
backup_dir="/mnt/backup/$(hostname)"
target_dir="$backup_dir/$cur_date"
dir_count=7

function backup {
    logger "Backup: starting."
    if [ ! -d $target_dir ]; then
        mkdir $target_dir
    fi

    cp -r /etc/openvpn $target_dir
    cp -r /home/ca $target_dir
    cp -r /var/log/openvpn $target_dir/logs
    logger "Backup: finish copy files"
}

function rotate_backup {
    # Ищем каталоги по маске (сортируем по имени=дате)
    # если их больше чем заданное количество копий,
    # то лишние (более старые) удаляем

    # Таким образом мы гарантированно имеем N-ое количество копий,
    # даже если по каким-то причинам бекапы перестали создаваться

    logger "Backup: Rotating directories"
    i=0
    for d in $(find $backup_dir -maxdepth 1 -type d -name "????_??_??"|sort -r)
    do
      let i++
      if [ $i -gt $dir_count ]; then
        logger "Backup: Remove $d"
        rm -rf "$d"
      fi
    done
}

if [ "$(df | grep '/mnt/backup')" ]; then
  if [ ! -d $backup_dir ]; then
    mkdir $backup_dir
  fi
  backup
  rotate_backup
else
  logger "Backup: Backup partition not mount! Stopping."
  exit 1
fi
