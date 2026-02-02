from enum import Enum


class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"  # Acceso a todas las compañías
    COMPANY_ADMIN = "company_admin"
    COMPANY_MANAGER = "company_manager"
    COMPANY_EMPLOYEE = "company_employee"
    CUSTOMER = "customer"


class Permission(str, Enum):
    # Permisos generales
    VIEW_DASHBOARD = "view_dashboard"
    
    # Permisos de productos
    VIEW_PRODUCTS = "view_products"
    CREATE_PRODUCTS = "create_products"
    EDIT_PRODUCTS = "edit_products"
    DELETE_PRODUCTS = "delete_products"
    
    # Permisos de órdenes
    VIEW_ORDERS = "view_orders"
    CREATE_ORDERS = "create_orders"
    EDIT_ORDERS = "edit_orders"
    DELETE_ORDERS = "delete_orders"
    
    # Permisos de usuarios
    VIEW_USERS = "view_users"
    CREATE_USERS = "create_users"
    EDIT_USERS = "edit_users"
    DELETE_USERS = "delete_users"
    
    # Permisos financieros
    VIEW_FINANCES = "view_finances"
    EDIT_FINANCES = "edit_finances"
