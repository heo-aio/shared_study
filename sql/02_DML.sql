/* 문자열 캐릭터셋 변경(latin1 -> utf8mb4)
 *sudo vim /tec/my.cnf
[mysqld]
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
추가 후 : wq

sudo systemctl restart mariadb
systemctl status mariadb
 * */

SHOW VARIABLES LIKE 'character_set%';

-- 캐릭터셋이 바뀌기 전에 만들어져버린 database와 table에 대해서 변경 (우리가 앞에서 먼저 만들어서)
ALTER DATABASE mydb CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE employees CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;


USE mydb;
SHOW tables;
-- INSERT
-- INSERT INTO [테이블명]([컬럼명, ...]) VALUES([값들, ...]);
INSERT INTO employees(
	emp_no, first_name, family_name, email, mobile, salary, depart_no, commission
)VALUES(
	111, '정모', '허', 'ppp97859@naver.com', '01046422532', '90000000', 'dev001', 90 
);

INSERT INTO employees(
	emp_no, first_name, family_name, email, mobile, salary
)VALUES(
	111, '영호', '이', 'godyh@naver.com', '01012345678', '1000000000' 
);

INSERT INTO employees(
	emp_no, family_name, email, mobile, salary
)VALUES(
	111, '이', 'godyh@naver.com', '01012345678', '1000000000' 
);

SELECT * FROM employees e;

-- UPDATE
-- UPDATE [테이블] SET [컬럼]=[값] WHERE [조건]
UPDATE employees SET depart_no = 'dev002' WHERE depart_no IS NULL;
UPDATE employees SET emp_no = 112 WHERE first_name = "영호";
UPDATE employees SET emp_no = 113 WHERE first_name IS NULL;
UPDATE employees SET commission = 10 WHERE commission IS NULL;

-- DELETE
-- DELETE FROM [테이블명] WHERE [조건]
DELETE FROM employees WHERE first_name IS NULL;

-- UPSERT (나중에 자세하게...)
-- 키가 중복되면 UPDATE, 중복되지 않으면 INSERT
-- 키가 없으면 실행할 수 없다.
INSERT INTO employees(emp_no, first_name, family_name, email, mobile, salary)
	VALUES(112, '영호', '김', 'email@naver.com', '01023125532', 5000000)
		ON DUPLICATE KEY UPDATE first_name = '상혁', family_name = '이';

DESC employees;






