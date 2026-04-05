-- 1. Desativar RLS da tabela (permite escrita pela chave anon/service_role)
ALTER TABLE vip_users DISABLE ROW LEVEL SECURITY;

-- 2. Inserir o email do dono diretamente
INSERT INTO vip_users (email, status)
VALUES ('thiagoimob2026@gmail.com', 'active')
ON CONFLICT (email) DO UPDATE SET status = 'active';

-- 3. Confirmar que entrou
SELECT * FROM vip_users;
