"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2026-05-30
"""
from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'deliverers',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('phone', sa.String(length=30), nullable=False),
        sa.Column('region', sa.String(length=80), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )
    op.create_table(
        'deliveries',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('order_id', sa.String(length=36), nullable=False, unique=True),
        sa.Column('region', sa.String(length=80), nullable=False),
        sa.Column('restaurant_id', sa.String(length=36), nullable=True),
        sa.Column('customer_id', sa.String(length=36), nullable=True),
        sa.Column('assigned_deliverer_id', sa.String(length=36), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('assigned_at', sa.DateTime(), nullable=True),
        sa.Column('picked_up_at', sa.DateTime(), nullable=True),
        sa.Column('delivered_at', sa.DateTime(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
    )
    op.create_table(
        'delivery_assignments',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('delivery_id', sa.String(length=36), nullable=False),
        sa.Column('deliverer_id', sa.String(length=36), nullable=True),
        sa.Column('assigned_by', sa.String(length=120), nullable=True),
        sa.Column('reason', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )


def downgrade():
    op.drop_table('delivery_assignments')
    op.drop_table('deliveries')
    op.drop_table('deliverers')
