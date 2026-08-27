from flask import Flask, render_template

# 애플리케이션 팩토리
def create_app():
    # 플라스크 애플리케이션을 생성
    app = Flask(__name__)

    # URL과 플라스크 코드를 매핑
#     @app.route('/')
#     def hello_pybo():
#         return 'Hello, Pybo!'
    from .views import main
    app.register_blueprint(main.bp)

    return app

if __name__ == '__main__':
    create_app.run(debug=True)