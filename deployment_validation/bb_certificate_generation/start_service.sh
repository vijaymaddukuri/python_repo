#!/usr/bin/expect
set ip [lindex $argv 0];
set username [lindex $argv 1];
set password [lindex $argv 2];
set prompt "(.*)(#|%|>|\\\$) $"
spawn ssh $username@$ip
expect "password"
send "$password\r"
expect -re $prompt
send "sudo systVIJAYtl restart  bridgeburner\r"
expect -re $prompt
puts $expect_out(1,string)
