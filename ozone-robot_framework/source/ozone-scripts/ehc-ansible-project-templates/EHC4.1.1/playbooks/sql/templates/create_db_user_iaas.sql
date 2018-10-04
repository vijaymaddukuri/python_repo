USE [$db_name]
CREATE LOGIN [$db_login_user] FROM WINDOWS
with DEFAULT_DATABASE=[$db_name]
go
EXEC master..sp_addsrvrolemember @loginame = N'$db_login_user', @rolename = N'$db_rolename'
Go