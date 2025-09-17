# Release Notes - yaml-to-backend v0.1.13

## 🎉 Major Bug Fixes and Improvements

### 🔧 Critical Fixes

#### **Entity Creation Issues Resolved**
- **Fixed Usuario entity creation**: Resolved `Column 'habilitado' cannot be null` error
- **Fixed Tarea entity creation**: Resolved `Column 'fecha_creacion' cannot be null` error
- **Root cause**: Model generator was incorrectly excluding required fields from Create models

#### **Configuration Initialization Order**
- **Fixed EntityParser initialization**: Moved initialization to `initialize()` method to ensure custom configuration is applied
- **Fixed ENTITIES_PATH resolution**: Now correctly uses custom paths instead of default `./entidades/`

### 🚀 Improvements

#### **Model Generator Enhancements**
- **Enhanced field processing**: Now correctly includes required fields in Create models
- **Improved datetime/boolean handling**: Fixed processing of datetime and boolean fields
- **Better field validation**: Respects `required: true` configuration from YAML files

#### **Backend Initialization**
- **Improved initialization sequence**: DatabaseManager and EntityParser now initialize with updated configuration
- **Better error handling**: More robust error handling during backend startup
- **Enhanced logging**: Better logging for debugging configuration issues

### ✅ Test Results

**All 9 entities now working perfectly:**
- ✅ SistemasOperativos: Complete CRUD operations
- ✅ Roles: Complete CRUD operations  
- ✅ **Usuario: Complete CRUD operations** (Previously failing)
- ✅ Aplicaciones: Complete CRUD operations
- ✅ Imagenes: Complete CRUD operations
- ✅ Contenedores: Complete CRUD operations
- ✅ Perfiles: Complete CRUD operations
- ✅ **Tarea: Complete CRUD operations** (Previously failing)
- ✅ AplicacionImagen: Complete CRUD operations

**Custom Routes:**
- ✅ All 6 custom routes functioning perfectly
- ✅ Authentication and JWT working correctly
- ✅ Permission system working as expected

### 🔄 Technical Changes

#### **Files Modified:**
- `yaml_to_backend/core/model_generator.py`: Fixed field inclusion logic
- `yaml_to_backend/app.py`: Fixed initialization order
- `yaml_to_backend/config.py`: Enhanced configuration handling
- `yaml_to_backend/__init__.py`: Updated imports and exports

#### **Key Code Changes:**
1. **Model Generator**: Removed incorrect exclusion of required fields
2. **Backend Generator**: Moved EntityParser initialization to `initialize()` method
3. **Configuration**: Enhanced `update_config()` function
4. **Field Processing**: Fixed datetime and boolean field handling

### 📦 Installation

```bash
pip install yaml-to-backend==0.1.13
```

### 🐛 Breaking Changes
- None

### 🔮 Migration Guide
- No migration required
- Existing YAML files will work without changes
- All existing functionality preserved

### 📝 Documentation
- Updated README with latest features
- Enhanced examples in documentation
- Improved error messages and logging

---

**Full Changelog**: https://github.com/cxmjg/yaml-to-backend/compare/v0.1.12...v0.1.13
