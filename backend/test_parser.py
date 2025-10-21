"""
Script simple para verificar que el parser XML funcione correctamente
"""
from xml_parser import XMLParser

print("="*60)
print("Verificando Parser XML")
print("="*60)

# Leer archivo
with open('ejemplo_configuracion.xml', 'r', encoding='utf-8') as f:
    xml_content = f.read()

print(f"\nTamaño del XML: {len(xml_content)} caracteres")

# Parsear
recursos, categorias, configuraciones, clientes = XMLParser.parsear_configuracion(xml_content)

# Ver resultados
print(f"\n✅ Recursos encontrados: {len(recursos)}")
print(f"✅ Categorías encontradas: {len(categorias)}")
print(f"✅ Configuraciones encontradas: {len(configuraciones)}")
print(f"✅ Clientes encontrados: {len(clientes)}")

# Detalles de recursos
if recursos:
    print("\n" + "-"*60)
    print("RECURSOS:")
    print("-"*60)
    for id, r in recursos.items():
        print(f"  [{id}] {r.nombre} ({r.abreviatura})")
        print(f"      Tipo: {r.tipo} | Métrica: {r.metrica}")
        print(f"      Costo: ${r.valor_x_hora}/hora")

# Detalles de clientes
if clientes:
    print("\n" + "-"*60)
    print("CLIENTES:")
    print("-"*60)
    for nit, c in clientes.items():
        print(f"  {c.nombre} (NIT: {nit})")
        print(f"  Usuario: {c.usuario}")
        print(f"  Instancias: {len(c.instancias)}")
        for id_inst, inst in c.instancias.items():
            print(f"    - [{id_inst}] {inst.nombre} ({inst.estado})")

print("\n" + "="*60)
print("Verificación completada")
print("="*60)