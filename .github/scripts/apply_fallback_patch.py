import sys
import os

scan_path = os.environ.get('SCAN_PATH', 'routes/login.ts')
if not os.path.isfile(scan_path):
    sys.exit(0)

with open(scan_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = "models.sequelize.query(`SELECT * FROM Users WHERE email = '${req.body.email || ''}' AND password = '${security.hash(req.body.password || '')}' AND deletedAt IS NULL`, { model: UserModel, plain: true })"
replacement = "models.sequelize.query('SELECT * FROM Users WHERE email = $1 AND password = $2 AND deletedAt IS NULL', { bind: [req.body.email || '', security.hash(req.body.password || '')], model: UserModel, plain: true })"

if target in content:
    with open(scan_path, 'w', encoding='utf-8') as f:
        f.write(content.replace(target, replacement))
    print(f"Applied fallback security patch to {scan_path}")
else:
    print(f"Target pattern not found in {scan_path}")
