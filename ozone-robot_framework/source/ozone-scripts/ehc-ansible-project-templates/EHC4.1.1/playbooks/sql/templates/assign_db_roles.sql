use $db_name
go
sp_addrolemember @rolename = '$db_rolename', @membername = '$db_login_user'
go