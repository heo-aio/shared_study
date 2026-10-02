-- 트랜잭션 : 쪼갤 수 없는 논리적 업무 단위
-- 실제로는 여러 단계이지만 한단계로 가정하는 것
-- 송금은 출금과 입금 두단계이지만, 둘 중 하나라도 실패하면 송금은 취소된다.
-- 이때 모든 작업을 확정하는 것을 commit
-- 작업을 취소하는 것을 rollback
-- SQL에선 무조건 commit을 해야 작업이 확정된다. (그런데 한 번도 한 적이 없다...?)

USE mydb;

-- 1) AUTOCOMMIT이 설정되어있어서 이다.
SELECT @@AUTOCOMMIT; -- 1: 설정 / 2: 미설정

-- 2) AUTOCOMMIT 변경
SET @@AUTOCOMMIT = 0;

COMMIT; -- 지금까지의 상태를 저장
DELETE FROM employees;
ROLLBACK;

SELECT * FROM employees e;