### Remember two things to setup a new database on a new server:

- Find/open postgresql.conf and change "listen_address='local host'" to "listen_address='*'"
- Find/open pg_hba.conf and add the developor's ipv4 address in the list such as "xxx.xxx.xx.x\0"