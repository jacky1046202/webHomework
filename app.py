from flask import Flask, render_template, redirect, url_for, request, flash
from config import Config
from models import db, Item

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()  # 初始化資料庫

# 主頁面 - 顯示商品清單
@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

# 新增商品頁面
@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        if name and price:
            try:
                price = float(price)
                item = Item(name=name, price=price)
                db.session.add(item)
                db.session.commit()
                flash("商品新增成功！", "success")
                return redirect(url_for('index'))
            except ValueError:
                flash("價格必須是數字！", "danger")
        else:
            flash("請填寫所有欄位！", "danger")
    return render_template('add_item.html')

# 刪除商品
@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("商品已刪除！", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
