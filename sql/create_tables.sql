-- PostgreSQL 建表脚本
-- 土地承包明细表

-- 如已存在则先删除（开发阶段使用，生产环境请注意数据安全）
-- DROP TABLE IF EXISTS contracts;

CREATE TABLE IF NOT EXISTS contracts (
    id          SERIAL PRIMARY KEY,                         -- 主键，自增
    name        VARCHAR(50)  NOT NULL,                      -- 承包人姓名
    land_location VARCHAR(200) NOT NULL,                    -- 地块位置
    id_card     VARCHAR(18)  NOT NULL,                      -- 身份证号（18位）
    phone       VARCHAR(11)  NOT NULL,                      -- 联系电话（11位）
    area        FLOAT        NOT NULL CHECK (area > 0),     -- 承包面积（亩），必须大于0
    year        INTEGER      NOT NULL
                    CHECK (year >= 1949 AND year <= 2100),  -- 承包年份
    remark      TEXT,                                       -- 备注（可选）
    village     VARCHAR(50)  NOT NULL,                      -- 村别
    bank_account VARCHAR(25),                               -- 银行卡号（可选）
    contractor_code VARCHAR(30) NOT NULL,                   -- 承包方编码
    plot_code   VARCHAR(30)  NOT NULL,                      -- 地块编码
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW(),        -- 创建时间
    updated_at  TIMESTAMP    NOT NULL DEFAULT NOW()         -- 更新时间
);

-- 承包人姓名索引（用于模糊搜索）
CREATE INDEX IF NOT EXISTS idx_contracts_name ON contracts (name);

-- 地块位置索引（用于模糊搜索）
CREATE INDEX IF NOT EXISTS idx_contracts_land_location ON contracts (land_location);

-- 创建时间索引（用于分页排序）
CREATE INDEX IF NOT EXISTS idx_contracts_created_at ON contracts (created_at DESC);

-- 自动更新 updated_at 字段的触发器函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 绑定触发器到 contracts 表
DROP TRIGGER IF EXISTS set_updated_at ON contracts;
CREATE TRIGGER set_updated_at
    BEFORE UPDATE ON contracts
    FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- 表注释
COMMENT ON TABLE contracts IS '土地承包明细表';
COMMENT ON COLUMN contracts.id IS '主键，自增';
COMMENT ON COLUMN contracts.name IS '承包人姓名';
COMMENT ON COLUMN contracts.land_location IS '地块位置';
COMMENT ON COLUMN contracts.id_card IS '身份证号（18位）';
COMMENT ON COLUMN contracts.phone IS '联系电话（11位纯数字）';
COMMENT ON COLUMN contracts.area IS '承包面积（亩）';
COMMENT ON COLUMN contracts.year IS '承包年份（1949~2100）';
COMMENT ON COLUMN contracts.remark IS '备注';
COMMENT ON COLUMN contracts.village IS '村别';
COMMENT ON COLUMN contracts.bank_account IS '银行卡号（可选）';
COMMENT ON COLUMN contracts.contractor_code IS '承包方编码';
COMMENT ON COLUMN contracts.plot_code IS '地块编码';
COMMENT ON COLUMN contracts.created_at IS '创建时间';
COMMENT ON COLUMN contracts.updated_at IS '最后更新时间';

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id               SERIAL PRIMARY KEY,                     -- 主键，自增
    username         VARCHAR(50) NOT NULL UNIQUE,            -- 用户名，唯一
    hashed_password  TEXT        NOT NULL,                   -- 哈希后的密码
    is_active        BOOLEAN     NOT NULL DEFAULT TRUE,      -- 是否激活
    created_at       TIMESTAMP   NOT NULL DEFAULT NOW()      -- 创建时间
);

-- 用户名索引
CREATE INDEX IF NOT EXISTS idx_users_username ON users (username);

-- 表注释
COMMENT ON TABLE users IS '用户表';
COMMENT ON COLUMN users.id IS '主键，自增';
COMMENT ON COLUMN users.username IS '用户名';
COMMENT ON COLUMN users.hashed_password IS '哈希后的密码';
COMMENT ON COLUMN users.is_active IS '是否激活';
COMMENT ON COLUMN users.created_at IS '创建时间';
