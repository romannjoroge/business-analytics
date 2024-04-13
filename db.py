from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List
from datetime import time

engine = create_engine("postgresql://postgres:example@localhost:5560", echo=True)

class Base(DeclarativeBase):
    pass

# Dim Counties table
class DimCounty(Base):
    __tablename__ = "dim_counties"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    cities: Mapped[List["DimCity"]] = relationship(back_populates="county")

    def __repr__(self):
        return f"<DimCounty name={self.name}>"

# Dim City table
class DimCity(Base):
    __tablename__ = "dim_cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    county: Mapped['DimCounty'] = relationship(back_populates="cities")
    stores: Mapped[List['DimStore']] = relationship(back_populates="city")

    def __repr__(self):
        return f"<DimCity county: {self.county.name} name: {self.name}>"

# Dim Store table
class DimStore(Base):
    __tablename__ = "dim_stores"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    city: Mapped['DimCity'] = relationship(back_populates="stores")
    employees: Mapped[List['DimEmployees']] = relationship(back_populates="store")
    sales: Mapped[List['FactSales']] = relationship(back_populates="store")

    def __repr__(self):
        return f"<DimStore name: {self.name} city: {self.city.name}"
 

# Dim employees table
class DimEmployees(Base):
    __tablename__ = "dim_employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    store: Mapped['DimStore'] = relationship(back_populates="employees")
    dob: Mapped[str] = mapped_column(default=time().isoformat())
    sales: Mapped[List['FactSales']] = relationship(back_populates="employee")

    def __repr__(self):
        return f"<DimEmployees name: {self.name} store_name: {self.store.name} dob: {self.dob}"
    
   
# Dim Product Categories Table
class DimProductCategories(Base):
    __tablename__ = "dim_product_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    products: Mapped[List['DimProducts']] = relationship(back_populates="category")

    def __repr__(self):
        return f"<DimProductCategories name={self.name}>"

# Dim Products table
class DimProducts(Base):
    __tablename__ = "dim_products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    category: Mapped['DimProductCategories'] = relationship(back_populates="products")
    sales: Mapped[List['FactSales']] = relationship(back_populates="product")

    def __repr__(self):
        return f"<DimStore name: {self.name} category_name: {self.category.name}"
    
# Dim Products table
class FactSales(Base):
    __tablename__ = "fact_sales"

    id: Mapped[int] = mapped_column(primary_key=True)
    product: Mapped['DimProducts'] = relationship(back_populates="sales")
    store: Mapped['DimStore'] = relationship(back_populates="sales")
    employee: Mapped['DimEmployees'] = relationship(back_populates="sales")
    quantity: Mapped[int] = mapped_column()
    price: Mapped[float] = mapped_column()
    soldAt: Mapped[str] = mapped_column(default=time().isoformat())

    def __repr__(self):
        return f"<FactSales product: {self.product.name} store: {self.store.name} employee: {self.employee.name} quantity: {self.quantity} price: {self.price} soldAt: {self.soldAtT}"

# Creates the tables    
Base.metadata.create_all(engine)