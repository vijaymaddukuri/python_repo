use [master]
go
CREATE DATABASE [$db_name] ON PRIMARY
(NAME = N'$db_name', FILENAME = N'$mdf_filepath$db_name.mdf', SIZE = $db_sizeinMBMB, FILEGROWTH = $db_fileGrowthPercentage% )
LOG ON
(NAME = N'$db_name_log', FILENAME = N'$ldf_filepath$db_name.ldf', SIZE = $log_sizeinKBKB, FILEGROWTH = $log_fileGrowthPercentage%)
COLLATE SQL_Latin1_General_CP1_CI_AS
Go