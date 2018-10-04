CREATE LOGIN [$db_login_user] FROM WINDOWS
with DEFAULT_DATABASE=$db_name, DEFAULT_LANGUAGE=$language
go
use $db_name
go 
CREATE USER [$db_login_user] for LOGIN [$db_login_user]
go