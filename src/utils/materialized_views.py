import sqlalchemy as sa
from sqlalchemy.schema import DDLElement
from sqlalchemy.ext import compiler
from src.database import Base  # Импортируем основную метадату


class CreateMaterializedView(DDLElement):
    def __init__(self, name, selectable):
        self.name = name
        self.selectable = selectable


class RefreshMaterializedView(DDLElement):
    def __init__(self, name):
        self.name = name


@compiler.compiles(CreateMaterializedView)
def _create_materialized_view(element, compiler, **kw):
    return "CREATE MATERIALIZED VIEW %s AS %s" % (
        element.name,
        compiler.sql_compiler.process(element.selectable, literal_binds=True),
    )


@compiler.compiles(RefreshMaterializedView)
def _refresh_materialized_view(element, compiler, **kw):
    return "REFRESH MATERIALIZED VIEW %s" % (element.name)


def materialized_view(name, selectable):
    """
    Создаёт объект материализованного представления в SQLAlchemy,
    используя основную метадату (Base.metadata).
    """
    view_table = sa.Table(
        name,
        sa.MetaData(),  # Убрал `metadata`, чтобы не зависеть от глобального объекта
        *[sa.Column(c.name, c.type) for c in selectable.selected_columns],
        extend_existing=True,
    )
    sa.event.listen(
        Base.metadata,
        "after_create",
        CreateMaterializedView(name, selectable).execute_if(dialect="postgresql"),
    )
    sa.event.listen(
        Base.metadata,
        "before_drop",
        sa.DDL(f"DROP MATERIALIZED VIEW IF EXISTS {name}").execute_if(
            dialect="postgresql"
        ),
    )
    return view_table
