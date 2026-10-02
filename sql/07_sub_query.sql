CREATE TABLE dept(
  deptno VARCHAR(10) PRIMARY KEY,
  deptname VARCHAR(20),
  loc VARCHAR(10)
);

-- 직원 테이블 생성
CREATE TABLE emp(
  ename varchar(20),
  job varchar(50),
  deptno VARCHAR(10),
  hiredate date
);

-- 키 설정
ALTER TABLE emp ADD CONSTRAINT fk_emp FOREIGN KEY(deptno) REFERENCES dept(deptno);


-- 데이터 삽입
INSERT INTO dept (deptno,deptname,loc)values(1, 'sales', 'NEWYORK');
INSERT INTO dept (deptno,deptname,loc)values(2, 'dev01', 'LA');
INSERT INTO dept (deptno,deptname,loc)values(3, 'personnel', 'NEWYORK');
INSERT INTO dept (deptno,deptname,loc)values(4, 'delevery', 'BOSTON');
SELECT * FROM dept;

INSERT INTO emp (ename,job,deptno,hiredate)values('kim', 'manager', 1, STR_TO_DATE('26/01/02','%Y/%m/%d'));
INSERT INTO emp (ename,job,deptno,hiredate)values('lee', 'staff', 1, STR_TO_DATE('25/01/02','%Y/%m/%d'));
INSERT INTO emp (ename,job,deptno,hiredate)values('han', 'staff', 1, STR_TO_DATE('26/03/02','%Y/%m/%d'));
INSERT INTO emp (ename,job,deptno,hiredate)values('kim', 'assistant', 1, STR_TO_DATE('15/09/22','%Y/%m/%d'));

INSERT INTO emp (ename,job,deptno,hiredate)values('ahn', 'staff', 2, STR_TO_DATE('25/11/02','%Y/%m/%d'));
INSERT INTO emp (ename,job,deptno,hiredate)values('hwang', 'manager', 2, STR_TO_DATE('25/08/12','%Y/%m/%d'));
INSERT INTO emp (ename,job,deptno,hiredate)values('cha', 'assistant', 2, STR_TO_DATE('22/03/02','%Y/%m/%d'));
INSERT INTO emp (ename,job,deptno,hiredate)values('hong', 'staff', 2, STR_TO_DATE('24/08/02','%Y/%m/%d'));
INSERT INTO emp (ename,job,deptno,hiredate)values('gang', 'staff', 2, STR_TO_DATE('26/01/02','%Y/%m/%d'));

INSERT INTO emp (ename,job,deptno,hiredate)values('nam', 'leader', 4, STR_TO_DATE('20/01/02','%Y/%m/%d'));
SELECT * FROM emp;

-- 문제 1) han의 근무부서 이름
SELECT * FROM emp;
SELECT * FROM dept;

SELECT deptno FROM emp
WHERE ename = "han";

-- 7 * (3 + 4) 이런 느낌
SELECT deptname FROM dept
WHERE deptno = (SELECT deptno FROM emp WHERE ename = "han");

-- 문제 2) 부서위치가 LA또는 BOSTON인 부서에 속한 사람들의 이름과 직책
SELECT deptno FROM dept
WHERE loc = "LA" OR loc = "BOSTON";

SELECT ename, job FROM emp
WHERE deptno IN (SELECT deptno FROM dept WHERE loc IN("LA", "BOSTON"));

-- 문제 3) sales 부서에 근무하는 사원의 이름, 직책, 입사일
SELECT deptno FROM dept
WHERE deptname = "sales";

SELECT ename, job, hiredate FROM emp
WHERE deptno = (SELECT deptno FROM dept WHERE deptname = "sales");

-- 문제 4) 직책이 MANAGER인 직원들(여려명일 경우 가장 빠른 사람 기준)보다 입사일이 빠른 사람들의 이름, 직책, 입사일
SELECT hiredate FROM emp
WHERE job = "manager"; -- 가장 빠른 날짜 2025-08-12

SELECT ename, job, hiredate FROM emp
WHERE hiredate < (SELECT hiredate FROM emp WHERE job = "manager" ORDER BY hiredate LIMIT 1);

SELECT ename, job, hiredate FROM emp
WHERE hiredate < (SELECT MIN(hiredate) FROM emp WHERE job = "manager" ORDER BY hiredate);

-- 문제 5) 부서별로 직원이 몇 명인지 알려주세요.
SELECT * FROM emp;
SELECT * FROM dept;

SELECT deptname FROM dept WHERE deptno = 1;

-- 서브쿼리가 메인쿼리의 일부가 되었다.
-- 상하 관계 쿼리
-- dept의 deptno가 오직 1만 나타남
SELECT deptname,
		(SELECT COUNT(deptno) FROM emp WHERE deptno = dept.deptno) as cnt
FROM dept WHERE deptno = 1;

SELECT deptname,
		-- 그렇게 불러온 deptno를 활용
		(SELECT COUNT(deptno) FROM emp WHERE deptno = dept.deptno) as cnt
FROM dept; -- dept의 모든 deptno를 불러옴

-- SELECT deptname FROM dept WHERE deptno = 1
SELECT
	e.deptno,
	(SELECT deptname FROM dept WHERE deptno = e.deptno) AS name,
	COUNT(e.deptno) AS cnt
FROM emp e GROUP BY  e.deptno;


SELECT deptno, COUNT(*) AS 2번부서cnt FROM emp WHERE deptno = 2;
SELECT deptno, COUNT(*) AS 3번부서cnt FROM emp WHERE deptno = 3;
SELECT deptno, COUNT(*) AS 4번부서cnt FROM emp WHERE deptno = 4;

SELECT COUNT(*) AS 직원수 FROM emp
GROUP BY job
ORDER BY COUNT(*);