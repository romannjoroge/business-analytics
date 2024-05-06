from sqlalchemy import create_engine, ForeignKey, text, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from typing import List
from datetime import time

engine = create_engine("postgresql://postgres:example@localhost:5560")
print("I AM UPDATED")
class Base(DeclarativeBase):
    pass

# Dim Counties table
class DimCounty(Base):
    __tablename__ = "dim_counties"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    cities: Mapped[List['DimCity']] = relationship(back_populates="county")

    def __repr__(self):
        return f"<DimCounty name={self.name}>"
    
class DimSuppliers (Base):
    __tablename__ = "dim_suppliers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    city_id: Mapped[int] = mapped_column(ForeignKey("dim_cities.id"))
    city: Mapped['DimCity'] = relationship(back_populates='suppliers')
    address: Mapped[str] = mapped_column()
    supplys: Mapped[List['FactSupplyOrder']] = relationship(back_populates='supplier')

    def __repr__(self):
        return f"<DimSuppliers name: {self.name} city_id: {self.city_id} address: {self.address}"

# Dim City table
class DimCity(Base):
    __tablename__ = "dim_cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    county_id: Mapped[int] = mapped_column(ForeignKey("dim_counties.id"))
    county: Mapped['DimCounty'] = relationship(back_populates='cities')
    stores: Mapped[List['DimStore']] = relationship(back_populates="city")
    suppliers: Mapped[List['DimSuppliers']] = relationship(back_populates="city")

    def __repr__(self):
        return f"<DimCity county: {self.county_id} name: {self.name}>"

# Dim Store table
class DimStore(Base):
    __tablename__ = "dim_stores"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    city_id: Mapped[int] = mapped_column(ForeignKey("dim_cities.id"))
    city: Mapped['DimCity'] = relationship(back_populates='stores')
    employees: Mapped[List['DimEmployees']] = relationship(back_populates="store")
    sales: Mapped['FactSales'] = relationship(back_populates="store")

    def __repr__(self):
        return f"<DimStore name: {self.name} city_id: {self.city_id}"
 

# Dim employees table
class DimEmployees(Base):
    __tablename__ = "dim_employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    store_id: Mapped[int] = mapped_column(ForeignKey("dim_stores.id"))
    dob: Mapped[str] = mapped_column(default=time().isoformat())
    store: Mapped['DimStore'] = relationship(back_populates="employees")
    sales: Mapped['FactSales'] = relationship(back_populates="employee")
    supplys: Mapped['FactSupplyOrder'] = relationship(back_populates="employee")

    def __repr__(self):
        return f"<DimEmployees name: {self.name} store_id: {self.store_id} dob: {self.dob}"
    
   
# Dim Product Categories Table
class DimProductCategories(Base):
    __tablename__ = "dim_product_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    products: Mapped[List['DimProducts']] = relationship(back_populates = "category")

    def __repr__(self):
        return f"<DimProductCategories name={self.name}>"

# Dim Products table
class DimProducts(Base):
    __tablename__ = "dim_products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey("dim_product_categories.id"))
    category: Mapped['DimProductCategories'] = relationship(back_populates = "products")
    sales: Mapped['FactSales'] = relationship(back_populates="product")
    supplys: Mapped[List['FactSupplyOrder']] = relationship(back_populates="product")

    def __repr__(self):
        return f"<DimStore name: {self.name} category_id: {self.category_id}"
    
# Dim Products table
class FactSales(Base):
    __tablename__ = "fact_sales"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("dim_products.id"))
    product: Mapped['DimProducts'] = relationship(back_populates = "sales")
    store_id: Mapped[int] = mapped_column(ForeignKey("dim_stores.id"))
    store: Mapped['DimStore'] = relationship(back_populates = "sales")
    employee_id: Mapped[int] = mapped_column(ForeignKey("dim_employees.id"))
    employee: Mapped['DimEmployees'] = relationship(back_populates = "sales")
    quantity: Mapped[int] = mapped_column()
    price: Mapped[float] = mapped_column()
    time: Mapped[str] = mapped_column()

    def __repr__(self):
        return f"<FactSales product_id: {self.product_id} store_id: {self.store_id} employee_id: {self.employee_id} quantity: {self.quantity} price: {self.price} soldAt: {self.soldAtT}"

class FactSupplyOrder(Base):
    __tablename__ = "fact_supply_order"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("dim_products.id"))
    product: Mapped['DimProducts'] = relationship(back_populates = "supplys")
    supplier_id: Mapped[int] = mapped_column(ForeignKey("dim_suppliers.id"))
    supplier: Mapped['DimSuppliers'] = relationship(back_populates = "supplys")
    employee_id: Mapped[int] = mapped_column(ForeignKey("dim_employees.id"))
    employee: Mapped['DimEmployees'] = relationship(back_populates = "supplys")
    quantity: Mapped[int] = mapped_column()
    price: Mapped[float] = mapped_column()
    time: Mapped[str] = mapped_column()


# Creates the tables    
Base.metadata.create_all(engine)