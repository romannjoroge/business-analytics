from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from typing import List
from datetime import time

engine = create_engine("postgresql://postgres:example@localhost:5560", echo=True)
print("I AM UPDATED")
class Base(DeclarativeBase):
    pass

# Dim Counties table
class DimCounty(Base):
    __tablename__ = "dim_counties"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    def __repr__(self):
        return f"<DimCounty name={self.name}>"

# Dim City table
class DimCity(Base):
    __tablename__ = "dim_cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    county_id: Mapped[int] = mapped_column(ForeignKey("dim_counties.id"))

    def __repr__(self):
        return f"<DimCity county: {self.county_id} name: {self.name}>"

# Dim Store table
class DimStore(Base):
    __tablename__ = "dim_stores"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    city_id: Mapped[int] = mapped_column(ForeignKey("dim_cities.id"))

    def __repr__(self):
        return f"<DimStore name: {self.name} city_id: {self.city_id}"
 

# Dim employees table
class DimEmployees(Base):
    __tablename__ = "dim_employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    store_id: Mapped[int] = mapped_column(ForeignKey("dim_stores.id"))
    dob: Mapped[str] = mapped_column(default=time().isoformat())

    def __repr__(self):
        return f"<DimEmployees name: {self.name} store_id: {self.store_id} dob: {self.dob}"
    
   
# Dim Product Categories Table
class DimProductCategories(Base):
    __tablename__ = "dim_product_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    def __repr__(self):
        return f"<DimProductCategories name={self.name}>"

# Dim Products table
class DimProducts(Base):
    __tablename__ = "dim_products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey("dim_product_categories.id"))

    def __repr__(self):
        return f"<DimStore name: {self.name} category_id: {self.category_id}"
    
# Dim Products table
class FactSales(Base):
    __tablename__ = "fact_sales"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("dim_products.id"))
    store_id: Mapped[int] = mapped_column(ForeignKey("dim_stores.id"))
    employee_id: Mapped[int] = mapped_column(ForeignKey("dim_employees.id"))
    quantity: Mapped[int] = mapped_column()
    price: Mapped[float] = mapped_column()
    soldAt: Mapped[str] = mapped_column(default=time().isoformat())

    def __repr__(self):
        return f"<FactSales product_id: {self.product_id} store_id: {self.store_id} employee_id: {self.employee_id} quantity: {self.quantity} price: {self.price} soldAt: {self.soldAtT}"

# Creates the tables    
Base.metadata.create_all(engine)