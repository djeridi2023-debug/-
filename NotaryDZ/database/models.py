from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, Text, ForeignKey, Enum, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime

Base = declarative_base()

# Association table for Acte and Client (Parties)
acte_parties = Table('acte_parties', Base.metadata,
    Column('acte_id', Integer, ForeignKey('actes.id')),
    Column('client_id', Integer, ForeignKey('clients.id')),
    Column('role', String(50)) # e.g., Vendeur, Acquereur
)

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    type_personne = Column(String(2)) # 'PH' or 'PM'
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100))
    raison_sociale = Column(String(200))
    num_nif = Column(String(20), unique=True)
    num_registre_commerce = Column(String(20))
    date_naissance = Column(Date)
    lieu_naissance = Column(String(100))
    adresse = Column(Text)
    aml_risk_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    actes = relationship("Acte", secondary=acte_parties, back_populates="parties")

class Acte(Base):
    __tablename__ = 'actes'
    id = Column(Integer, primary_key=True)
    type_acte = Column(String(20)) # VENTE, DON, etc.
    date_acte = Column(Date, default=datetime.date.today)
    numero_repertoire = Column(String(50), unique=True)
    contenu_texte = Column(Text)
    contenu_hashed = Column(String(256))
    ai_summary = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    parties = relationship("Client", secondary=acte_parties, back_populates="actes")
    transaction_fonciere = relationship("TransactionFonciere", uselist=False, back_populates="acte")

class TransactionFonciere(Base):
    __tablename__ = 'transactions_foncieres'
    id = Column(Integer, primary_key=True)
    acte_id = Column(Integer, ForeignKey('actes.id'))
    reference_fonciere = Column(String(100))
    date_depot = Column(Date)
    statut_publication = Column(String(50))

    acte = relationship("Acte", back_populates="transaction_fonciere")

# Database setup
engine = create_engine('sqlite:///notary_dz.db')
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
