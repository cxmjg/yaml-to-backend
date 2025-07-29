#!/bin/bash

# Script para ejecutar pruebas curl del backend IPAS
# Autor: Sistema IPAS
# Fecha: $(date)

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración
BASE_URL="http://localhost:8001"
ADMIN_USER="admin"
ADMIN_PASS="admin123"
USER1="usuario1"
USER1_PASS="usuario123"

# Variables para tokens y IDs creados
ADMIN_TOKEN=""
USER1_TOKEN=""
CREATED_USER_ID=""
CREATED_TASK_ID=""

# Función para imprimir mensajes
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Función para verificar si el backend está ejecutándose
check_backend() {
    print_status "Verificando si el backend está ejecutándose..."
    
    if curl -s "$BASE_URL/" > /dev/null 2>&1; then
        print_success "Backend está ejecutándose en $BASE_URL"
        return 0
    else
        print_error "Backend no está ejecutándose en $BASE_URL"
        print_warning "Asegúrate de que el backend esté iniciado con: python main.py"
        return 1
    fi
}

# Función para obtener token de autenticación
get_token() {
    local username=$1
    local password=$2
    local token_var=$3
    
    print_status "Obteniendo token para usuario: $username"
    
    local response=$(curl -s -X POST "$BASE_URL/api/auth/login" \
        -H "Content-Type: application/json" \
        -d "{\"username\": \"$username\", \"password\": \"$password\"}")
    
    if echo "$response" | grep -q "access_token"; then
        local token=$(echo "$response" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
        eval "$token_var=\"$token\""
        print_success "Token obtenido para $username"
        return 0
    else
        print_error "Error obteniendo token para $username: $response"
        return 1
    fi
}

# Función para probar endpoint de salud
test_health() {
    print_status "Probando endpoint de salud..."
    
    local response=$(curl -s "$BASE_URL/")
    if echo "$response" | grep -q "Backend funcionando correctamente"; then
        print_success "Endpoint de salud: OK"
        echo "Respuesta: $response"
    else
        print_error "Endpoint de salud: FALLÓ"
        echo "Respuesta: $response"
    fi
    echo
}

# Función para probar login
test_login() {
    print_status "Probando login de usuarios..."
    
    # Probar login admin
    print_status "Probando login admin..."
    if get_token "$ADMIN_USER" "$ADMIN_PASS" "ADMIN_TOKEN"; then
        print_success "Login admin: OK"
    else
        print_error "Login admin: FALLÓ"
    fi
    
    # Probar login usuario1
    print_status "Probando login usuario1..."
    if get_token "$USER1" "$USER1_PASS" "USER1_TOKEN"; then
        print_success "Login usuario1: OK"
    else
        print_error "Login usuario1: FALLÓ"
    fi
    echo
}

# Función para probar endpoint /api/auth/me
test_me_endpoint() {
    print_status "Probando endpoint /api/auth/me..."
    
    if [ -n "$ADMIN_TOKEN" ]; then
        print_status "Probando /api/auth/me con token admin..."
        local response=$(curl -s -X GET "$BASE_URL/api/auth/me" \
            -H "Authorization: Bearer $ADMIN_TOKEN")
        
        if echo "$response" | grep -q "username.*admin"; then
            print_success "/api/auth/me admin: OK"
            echo "Respuesta: $response"
        else
            print_error "/api/auth/me admin: FALLÓ"
            echo "Respuesta: $response"
        fi
    fi
    
    if [ -n "$USER1_TOKEN" ]; then
        print_status "Probando /api/auth/me con token usuario1..."
        local response=$(curl -s -X GET "$BASE_URL/api/auth/me" \
            -H "Authorization: Bearer $USER1_TOKEN")
        
        if echo "$response" | grep -q "username.*usuario1"; then
            print_success "/api/auth/me usuario1: OK"
            echo "Respuesta: $response"
        else
            print_error "/api/auth/me usuario1: FALLÓ"
            echo "Respuesta: $response"
        fi
    fi
    echo
}

# Función para probar endpoints CRUD completos de usuarios
test_usuario_crud_complete() {
    print_status "Probando endpoints CRUD completos de usuarios..."
    
    if [ -n "$ADMIN_TOKEN" ]; then
        # 1. Listar usuarios
        print_status "Probando GET /api/usuario/ con token admin..."
        local response=$(curl -s -X GET "$BASE_URL/api/usuario/?skip=0&limit=10" \
            -H "Authorization: Bearer $ADMIN_TOKEN")
        
        if echo "$response" | grep -q "detail.*No se pudieron validar las credenciales"; then
            print_error "GET /api/usuario/ admin: FALLÓ - Error de autenticación"
        else
            print_success "GET /api/usuario/ admin: OK"
            echo "Respuesta: $response"
        fi
        
        # 2. Crear usuario
        print_status "Probando POST /api/usuario/ con token admin..."
        local create_response=$(curl -s -X POST "$BASE_URL/api/usuario/" \
            -H "Authorization: Bearer $ADMIN_TOKEN" \
            -H "Content-Type: application/json" \
            -d "{\"username\": \"nuevo_usuario_$(date +%s)\", \"password\": \"password123\", \"rol\": \"usuario\"}")
        
        if echo "$create_response" | grep -q "detail.*No se pudieron validar las credenciales"; then
            print_error "POST /api/usuario/ admin: FALLÓ - Error de autenticación"
        elif echo "$create_response" | grep -q '"id"'; then
            print_success "POST /api/usuario/ admin: OK"
            echo "Respuesta: $create_response"
            # Extraer ID del usuario creado
            CREATED_USER_ID=$(echo "$create_response" | grep -o '"id":[0-9]*' | cut -d':' -f2)
            print_status "Usuario creado con ID: $CREATED_USER_ID"
            
            # 3. Obtener usuario por ID
            print_status "Probando GET /api/usuario/$CREATED_USER_ID con token admin..."
            local get_response=$(curl -s -X GET "$BASE_URL/api/usuario/$CREATED_USER_ID" \
                -H "Authorization: Bearer $ADMIN_TOKEN")
            
            if echo "$get_response" | grep -q '"username":"nuevo_usuario_'; then
                print_success "GET /api/usuario/$CREATED_USER_ID admin: OK"
                echo "Respuesta: $get_response"
            else
                print_error "GET /api/usuario/$CREATED_USER_ID admin: FALLÓ"
                echo "Respuesta: $get_response"
            fi
            
            # 4. Actualizar usuario
            print_status "Probando PUT /api/usuario/$CREATED_USER_ID con token admin..."
            local update_response=$(curl -s -X PUT "$BASE_URL/api/usuario/$CREATED_USER_ID" \
                -H "Authorization: Bearer $ADMIN_TOKEN" \
                -H "Content-Type: application/json" \
                -d "{\"username\": \"usuario_actualizado_$(date +%s)\", \"password\": \"password123\", \"rol\": \"admin\"}")
            
            if echo "$update_response" | grep -q '"rol":"admin"'; then
                print_success "PUT /api/usuario/$CREATED_USER_ID admin: OK"
                echo "Respuesta: $update_response"
            else
                print_error "PUT /api/usuario/$CREATED_USER_ID admin: FALLÓ"
                echo "Respuesta: $update_response"
            fi
            
            # 5. Eliminar usuario
            print_status "Probando DELETE /api/usuario/$CREATED_USER_ID con token admin..."
            local delete_response=$(curl -s -X DELETE "$BASE_URL/api/usuario/$CREATED_USER_ID" \
                -H "Authorization: Bearer $ADMIN_TOKEN")
            
            if [ "$(echo "$delete_response" | wc -c)" -le 1 ] || echo "$delete_response" | grep -q '"deleted_at"' || echo "$delete_response" | grep -q '"message"'; then
                print_success "DELETE /api/usuario/$CREATED_USER_ID admin: OK"
            else
                print_error "DELETE /api/usuario/$CREATED_USER_ID admin: FALLÓ"
                echo "Respuesta: $delete_response"
            fi
        else
            print_error "POST /api/usuario/ admin: FALLÓ"
            echo "Respuesta: $create_response"
        fi
    fi
    echo
}

# Función para probar endpoints CRUD completos de tareas
test_tarea_crud_complete() {
    print_status "Probando endpoints CRUD completos de tareas..."
    
    if [ -n "$USER1_TOKEN" ]; then
        # 1. Listar tareas
        print_status "Probando GET /api/tarea/ con token usuario1..."
        local response=$(curl -s -X GET "$BASE_URL/api/tarea/?skip=0&limit=10" \
            -H "Authorization: Bearer $USER1_TOKEN")
        
        if echo "$response" | grep -q "detail.*No se pudieron validar las credenciales"; then
            print_error "GET /api/tarea/ usuario1: FALLÓ - Error de autenticación"
        else
            print_success "GET /api/tarea/ usuario1: OK"
            echo "Respuesta: $response"
        fi
        
        # 2. Crear tarea
        print_status "Probando POST /api/tarea/ con token usuario1..."
        local create_response=$(curl -s -X POST "$BASE_URL/api/tarea/" \
            -H "Authorization: Bearer $USER1_TOKEN" \
            -H "Content-Type: application/json" \
            -d '{"titulo": "Nueva tarea de prueba", "descripcion": "Descripción de la nueva tarea", "usuario_id": 2, "completada": false}')
        
        if echo "$create_response" | grep -q "detail.*No se pudieron validar las credenciales"; then
            print_error "POST /api/tarea/ usuario1: FALLÓ - Error de autenticación"
        elif echo "$create_response" | grep -q '"id"'; then
            print_success "POST /api/tarea/ usuario1: OK"
            echo "Respuesta: $create_response"
            # Extraer ID de la tarea creada
            CREATED_TASK_ID=$(echo "$create_response" | grep -o '"id":[0-9]*' | cut -d':' -f2)
            print_status "Tarea creada con ID: $CREATED_TASK_ID"
            
            # 3. Obtener tarea por ID
            print_status "Probando GET /api/tarea/$CREATED_TASK_ID con token usuario1..."
            local get_response=$(curl -s -X GET "$BASE_URL/api/tarea/$CREATED_TASK_ID" \
                -H "Authorization: Bearer $USER1_TOKEN")
            
            if echo "$get_response" | grep -q '"titulo":"Nueva tarea de prueba"'; then
                print_success "GET /api/tarea/$CREATED_TASK_ID usuario1: OK"
                echo "Respuesta: $get_response"
            else
                print_error "GET /api/tarea/$CREATED_TASK_ID usuario1: FALLÓ"
                echo "Respuesta: $get_response"
            fi
            
            # 4. Actualizar tarea
            print_status "Probando PUT /api/tarea/$CREATED_TASK_ID con token usuario1..."
            local update_response=$(curl -s -X PUT "$BASE_URL/api/tarea/$CREATED_TASK_ID" \
                -H "Authorization: Bearer $USER1_TOKEN" \
                -H "Content-Type: application/json" \
                -d '{"titulo": "Tarea actualizada", "descripcion": "Descripción actualizada", "completada": true}')
            
            if echo "$update_response" | grep -q '"completada":true'; then
                print_success "PUT /api/tarea/$CREATED_TASK_ID usuario1: OK"
                echo "Respuesta: $update_response"
            else
                print_error "PUT /api/tarea/$CREATED_TASK_ID usuario1: FALLÓ"
                echo "Respuesta: $update_response"
            fi
            
            # 5. Eliminar tarea
            print_status "Probando DELETE /api/tarea/$CREATED_TASK_ID con token usuario1..."
            local delete_response=$(curl -s -X DELETE "$BASE_URL/api/tarea/$CREATED_TASK_ID" \
                -H "Authorization: Bearer $USER1_TOKEN")
            
            if [ "$(echo "$delete_response" | wc -c)" -le 1 ] || echo "$delete_response" | grep -q '"deleted_at"' || echo "$delete_response" | grep -q '"message"'; then
                print_success "DELETE /api/tarea/$CREATED_TASK_ID usuario1: OK"
            else
                print_error "DELETE /api/tarea/$CREATED_TASK_ID usuario1: FALLÓ"
                echo "Respuesta: $delete_response"
            fi
        else
            print_error "POST /api/tarea/ usuario1: FALLÓ"
            echo "Respuesta: $create_response"
        fi
    fi
    echo
}

# Función para probar endpoints /yo
test_yo_endpoints() {
    print_status "Probando endpoints /yo..."
    
    if [ -n "$USER1_TOKEN" ]; then
        # Probar /api/tarea/yo
        print_status "Probando GET /api/tarea/yo con token usuario1..."
        local response=$(curl -s -X GET "$BASE_URL/api/tarea/yo?skip=0&limit=10" \
            -H "Authorization: Bearer $USER1_TOKEN")
        
        if echo "$response" | grep -q "detail.*No se pudieron validar las credenciales"; then
            print_error "GET /api/tarea/yo usuario1: FALLÓ - Error de autenticación"
        else
            print_success "GET /api/tarea/yo usuario1: OK"
            echo "Respuesta: $response"
        fi
        
        # Probar /api/usuario/yo
        print_status "Probando GET /api/usuario/yo con token usuario1..."
        local response=$(curl -s -X GET "$BASE_URL/api/usuario/yo" \
            -H "Authorization: Bearer $USER1_TOKEN")
        
        if echo "$response" | grep -q "detail.*No se pudieron validar las credenciales"; then
            print_error "GET /api/usuario/yo usuario1: FALLÓ - Error de autenticación"
        else
            print_success "GET /api/usuario/yo usuario1: OK"
            echo "Respuesta: $response"
        fi
    fi
    echo
}

# Función para probar acceso sin autenticación
test_unauthorized_access() {
    print_status "Probando acceso sin autenticación..."
    
    # Probar /api/auth/me sin token
    local response=$(curl -s -X GET "$BASE_URL/api/auth/me")
    if echo "$response" | grep -q "detail.*Not authenticated"; then
        print_success "Acceso no autenticado a /api/auth/me: OK (rechazado correctamente)"
    else
        print_error "Acceso no autenticado a /api/auth/me: FALLÓ"
        echo "Respuesta: $response"
    fi
    
    # Probar /api/usuario/ sin token
    local response=$(curl -s -X GET "$BASE_URL/api/usuario/")
    if echo "$response" | grep -q "detail.*Not authenticated"; then
        print_success "Acceso no autenticado a /api/usuario/: OK (rechazado correctamente)"
    else
        print_error "Acceso no autenticado a /api/usuario/: FALLÓ"
        echo "Respuesta: $response"
    fi
    
    # Probar /api/tarea/ sin token
    local response=$(curl -s -X GET "$BASE_URL/api/tarea/")
    if echo "$response" | grep -q "detail.*Not authenticated"; then
        print_success "Acceso no autenticado a /api/tarea/: OK (rechazado correctamente)"
    else
        print_error "Acceso no autenticado a /api/tarea/: FALLÓ"
        echo "Respuesta: $response"
    fi
    echo
}

# Función para probar tokens inválidos
test_invalid_tokens() {
    print_status "Probando tokens inválidos..."
    
    # Probar /api/usuario/ con token inválido
    local response=$(curl -s -X GET "$BASE_URL/api/usuario/" \
        -H "Authorization: Bearer token_invalido")
    if echo "$response" | grep -q "detail.*No se pudieron validar las credenciales"; then
        print_success "Token inválido en /api/usuario/: OK (rechazado correctamente)"
    else
        print_error "Token inválido en /api/usuario/: FALLÓ"
        echo "Respuesta: $response"
    fi
    
    # Probar /api/tarea/ con token inválido
    local response=$(curl -s -X GET "$BASE_URL/api/tarea/" \
        -H "Authorization: Bearer token_invalido")
    if echo "$response" | grep -q "detail.*No se pudieron validar las credenciales"; then
        print_success "Token inválido en /api/tarea/: OK (rechazado correctamente)"
    else
        print_error "Token inválido en /api/tarea/: FALLÓ"
        echo "Respuesta: $response"
    fi
    echo
}

# Función principal
main() {
    echo "=========================================="
    echo "    PRUEBAS CURL - BACKEND IPAS"
    echo "=========================================="
    echo
    
    # Verificar backend
    if ! check_backend; then
        exit 1
    fi
    
    # Ejecutar pruebas en el mismo orden que Postman
    test_health
    test_login
    test_me_endpoint
    test_usuario_crud_complete
    test_tarea_crud_complete
    test_yo_endpoints
    test_unauthorized_access
    test_invalid_tokens
    
    echo "=========================================="
    echo "    PRUEBAS COMPLETADAS"
    echo "=========================================="
    print_status "Revisa los resultados arriba para verificar el estado del backend"
    print_status "Pruebas ejecutadas:"
    print_status "  ✅ Health Check"
    print_status "  ✅ Login (Admin y Usuario)"
    print_status "  ✅ Get Current User (/api/auth/me)"
    print_status "  ✅ Usuario CRUD completo (Listar, Crear, Obtener, Actualizar, Eliminar)"
    print_status "  ✅ Tarea CRUD completo (Listar, Crear, Obtener, Actualizar, Eliminar)"
    print_status "  ✅ Endpoints /yo (Mis tareas y Mi usuario)"
    print_status "  ✅ Acceso sin autenticación"
    print_status "  ✅ Tokens inválidos"
}

# Ejecutar función principal
main "$@" 