from sqlalchemy import create_engine

from fastapi_amis_admin.admin import admin, AdminSite, AdminApp
from tests.models import User

class UserAdmin(admin.ModelAdmin):
    model = User

class BlogApp(admin.AdminApp):

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.register_admin(UserAdmin)

async def test_register_admin(site: AdminSite):
    app = site.get_admin_or_create(BlogApp)
    assert app.db
    assert app.engine
    ins = app.get_admin_or_create(UserAdmin)
    assert ins in app
    assert app.get_model_admin(User.__tablename__)

    site.register_router()
    assert site.get_model_admin(User.__tablename__)

    site.unregister_admin(BlogApp)
    app = site.get_admin_or_create(BlogApp, register = False)
    assert app is None

async def test_get_model_admin(site: AdminSite):
    BlogApp.engine = create_engine('sqlite:///amisadmin2.db?check_same_thread=False')
    site.register_admin(BlogApp)
    site.register_router()
    assert site.get_model_admin(User.__tablename__) is None

    app = site.get_admin_or_create(BlogApp)
    assert app.get_model_admin(User.__tablename__)

async def test__get_page_as_app(site: AdminSite):
    pass

async def test__get_page_as_tabs(site: AdminSite):
    pass
