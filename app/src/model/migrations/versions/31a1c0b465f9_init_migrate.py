"""init migrate

Revision ID: 31a1c0b465f9
Revises: 
Create Date: 2025-05-20 23:05:00.080199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31a1c0b465f9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('data_sensor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('suhu', sa.Float(), nullable=True),
    sa.Column('kelembapan_udara', sa.Float(), nullable=True),
    sa.Column('kelembapan_tanah', sa.Float(), nullable=True),
    sa.Column('penyiraman', sa.Boolean(), nullable=True),
    sa.Column('pengkabutan', sa.Boolean(), nullable=True),
    sa.Column('dibuat_sejak', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('jadwal_penyiraman',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('waktu_1', sa.Time(timezone=True), nullable=True),
    sa.Column('waktu_2', sa.Time(timezone=True), nullable=True),
    sa.Column('jenis_aksi', sa.Enum('penyiraman', 'pengkabutan', name='jenis_aksi_enum'), nullable=True),
    sa.Column('dibuat_sejak', sa.DateTime(timezone=True), nullable=True),
    sa.Column('diubah_sejak', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('nomor_hp',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nomor_hp', sa.String(length=15), nullable=False),
    sa.Column('dibuat_sejak', sa.DateTime(timezone=True), nullable=True),
    sa.Column('diubah_sejak', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nomor_hp')
    )
    op.create_table('riwayat_aksi',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jenis_aksi', sa.Enum('penyiraman', 'pengkabutan', name='riwayat_aksi_enum'), nullable=True),
    sa.Column('status', sa.Enum('aktif', 'nonaktif', name='status_aksi_enum'), nullable=True),
    sa.Column('dibuat_sejak', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('riwayat_aksi')
    op.drop_table('nomor_hp')
    op.drop_table('jadwal_penyiraman')
    op.drop_table('data_sensor')
    # ### end Alembic commands ###
