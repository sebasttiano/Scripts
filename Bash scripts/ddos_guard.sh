#!/bin/bash

#show help
function show_help()
{
  echo "NAME:" 
  echo -e "\t$0" 
  echo 'SYNOPSIS:'
  echo -e "\t$0 server ip enable|disable"
  echo 'EXAMPLE:'
  echo -e "\t$0 ava 2.59.43.100 enable"
  echo "DESCRIPTION:" 
  echo -e "\tenable or disable ddos guard " 
}

if [ "$#" -ne 3 ]; then
  echo "Illegal number of parameters" 
  show_help
  exit 25
fi

if [[ $3 == "enable" ]]; then
ssh $1 << EOF
  # вешаем ip адрес на интерфейс
  ip a a ${2}/24 dev eth0
  # создание доп.таблицы
  echo "100 ddos_guard" >> /etc/iproute2/rt_tables
  # Добавляем маршрут по умолчанию в новую таблицу
  ip route add default via 2.59.43.1 dev eth0 table 100
  # Добавляем правило, что для трафика с любого ip "защищенной" подсети маршрут брать из таблицы 100
  ip rule add from 2.59.43.0/24 table 100
  # добавляем защищенный IP адрес
  echo "listen ${2}:80;" > /etc/nginx/ddos_guard_http_ip.conf
  echo "listen ${2}:443;" > /etc/nginx/ddos_guard_https_ip.conf
  # релоудим nginx
  service nginx reload
EOF
elif [[ $3 == "disable" ]]; then
ssh $1 << EOF
  # вешаем ip адрес на интерфейс
  ip a d ${2}/24 dev eth0
  # Удаляем правило, что для трафика с любого ip "защищенной" подсети маршрут брать из таблицы 100
  ip rule delete from 2.59.43.0/24 table 100
  # Удаляем маршрут по умолчанию в новую таблицу
  ip route delete default via 2.59.43.1 dev eth0 table 100
  # Удаляем доп.таблицы
  sed -i '/100 ddos_guard/d' /etc/iproute2/rt_tables
  # очищаем ddos_guard_http*_ip.conf
  > /etc/nginx/ddos_guard_http_ip.conf
  > /etc/nginx/ddos_guard_https_ip.conf
  # релоудим nginx
  service nginx reload
EOF
fi
