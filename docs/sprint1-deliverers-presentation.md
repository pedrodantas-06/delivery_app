# 🎤 Apresentação — Deliverers MVP Sprint 1

## 📌 Cenário Principal Escolhido

**Scenario: Atribuir entregador automaticamente**

Este é o cenário mais forte porque:
- Demonstra a **lógica de negócio core** (assignment)
- Integra **múltiplas camadas** (Service → Repository → Database)
- Valida **regras de validação** (região, status disponível)
- Mostra **transação bem-sucedida** (ordem + entregador sincronizados)

### Fluxo BDD

```gherkin
Scenario: atribuir entregador automaticamente
  Given uma ordem pendente na regiao "Zona Sul"
  And um entregador disponivel na regiao "Zona Sul"
  When a atribuicao automatica for solicitada para a ordem
  Then a ordem deve ser marcada como "IN_DELIVERY"
  And o entregador deve ser marcado como "OCCUPIED"
```

---

## 🏗️ Explicar Backend — Fluxo Completo

### Passo a Passo: Request → Database

```
1. HTTP REQUEST
   POST /api/orders/assign/
   {
     "order_id": "uuid",
     "region": "Zona Sul"
   }
   ↓
   
2. VIEW LAYER (http/views/deliverers_views.py)
   - Parse JSON body
   - Validate required fields (order_id, region)
   - Call service.assign_deliverer()
   - Return JSON response with order status
   ↓
   
3. SERVICE LAYER (application/services/deliverers_service.py)
   - Validate business logic:
     - Check if order exists
     - Find available deliverer by region
     - Check if deliverer.status == AVAILABLE
     - Mark deliverer as OCCUPIED
   - Orchestrate repository calls
   - Return updated Order entity
   ↓
   
4. REPOSITORY LAYER (infrastructure/repositories.py)
   - DelivererRepositoryImpl.find_available_by_region(region)
     - Query: DelivererModel.objects.filter(
         region=region,
         status="AVAILABLE"
       )
     - Convert DB row → Deliverer entity
   - DelivererRepositoryImpl.save(occupied_deliverer)
     - Update: DelivererModel.objects.update_or_create(...)
   - OrderRepositoryImpl.save(assigned_order)
     - Update: OrderModel.objects.update_or_create(...)
   ↓
   
5. DATABASE LAYER (PostgreSQL)
   - UPDATE deliverers SET status='OCCUPIED' WHERE id=?
   - UPDATE orders SET status='IN_DELIVERY', assigned_deliverer_id=? WHERE id=?
   ↓
   
6. HTTP RESPONSE (200 OK)
   {
     "order_id": "uuid",
     "status": "IN_DELIVERY",
     "assigned_deliverer_id": "uuid"
   }
```

---

## 📦 Arquivos Criados & Responsabilidades

| Arquivo | Responsabilidade | Camada |
|---------|-----------------|--------|
| `domain/entities.py` | Deliverer, Order domain objects (DTOs tipadas) | Domain |
| `domain/enums.py` | DelivererStatus, OrderStatus enums | Domain |
| `domain/ports.py` | Abstract DelivererRepository, OrderRepository interfaces | Domain |
| `infrastructure/models/deliverers_model.py` | Django ORM models (DB schema) | Infrastructure |
| `infrastructure/repositories.py` | DelivererRepositoryImpl, OrderRepositoryImpl (DB queries) | Infrastructure |
| `application/services/deliverers_service.py` | DelivererService (business logic) | Application |
| `http/views/deliverers_views.py` | REST endpoints, request/response handling | HTTP |
| `http/urls.py` | URL routing for deliverers endpoints | HTTP |
| `wires.py` | Dependency injection setup | Wiring |
| `tests/features/deliverers.feature` | BDD scenarios in Gherkin | Test |
| `tests/steps/test_deliverers_steps.py` | Step implementations (pytest-bdd) | Test |
| `migrations/0001_initial.py` | Initial table creation | Migration |
| `migrations/0002_deliverer_created_at.py` | Add created_at column | Migration |

---

## 📈 Evolução por Commits

### Commit 1: `feat: create deliverer model and migration`
**O que foi feito:**
- Created Deliverer domain entity (dataclass)
- Created DelivererModel Django ORM model
- Added fields: id, name, phone, region, status, created_at
- Created OrderModel for order data

**Por que:**
- Models são a base: definem estrutura de dados
- Domain entities facilitam type safety
- Migrations versionar schema changes

---

### Commit 2: `feat: implement deliverer repository with data access`
**O que foi feito:**
- Created DelivererRepositoryImpl (abstract interface via ports)
- Implemented save(), get_by_id(), list_deliverers(), find_available_by_region()
- Created OrderRepositoryImpl for order persistence
- Abstracted DB queries behind clean interface

**Por que:**
- Repository pattern encapsula DB access
- Ports/interfaces permitem testing (mock repositories)
- Separação de concerns (domain logic ≠ db queries)

---

### Commit 3: `feat: implement deliverer service with core operations`
**O que foi feito:**
- Created DelivererService (business logic layer)
- Implemented register_deliverer(), update_status(), list_deliverers()
- Implemented assign_deliverer() (auto + manual assignment)
- Implemented reassign_deliverer() (after refusal)
- Injected dependencies (DelivererRepository, OrderRepository)

**Por que:**
- Service orchestrates use cases
- Business rules são centralizadas
- Easy to test (depends on abstract repositories)
- Dependency injection via wires.py

---

### Commit 4: `test: implement bdd step definitions`
**O que foi feito:**
- Implemented all 8 BDD steps for deliverers.feature
- Connected pytest-bdd scenarios to test code
- Mocked HTTP requests via Django test client
- Validated response structures

**Por que:**
- BDD closes gap entre stakeholders + code
- Steps are reusable across scenarios
- Test coverage for all Happy/Sad paths

---

### Commit 5: `feat: add database migration for deliverer created_at field`
**O que foi feito:**
- Created migration 0002_deliverer_created_at
- Added created_at timestamp to DelivererModel
- Updated domain entity to include created_at

**Por que:**
- Audit trail (when was deliverer registered?)
- Separate migration for clean version control
- Good practice for data integrity

---

## ✅ Critério de Sucesso

### Validação Técnica
- **✅ Testes BDD**: 8 cenários implementados e pronto para rodar
- **✅ Docker**: Estrutura pronta (PostgreSQL + Django)
- **✅ Migrações**: 2 migrations versionadas
- **✅ Sem complexidade desnecessária**: Sem events, messaging, CQRS, observables

### Validação de Arquitetura
- **✅ Nomenclatura**: 100% em inglês no código (entidades, métodos, variáveis)
- **✅ Separação de concerns**: Domain → Service → Repository → Model (4 camadas)
- **✅ Baixo acoplamento**: Via abstract repositories (ports)
- **✅ Extensibilidade**: Fácil adicionar novo provider de dados

### Validação de Negócio (Sprint 1)
- **✅ CRUD básico**: Register, list, update status ✓
- **✅ Atribuição automática**: Find available by region ✓
- **✅ Atribuição manual**: Check availability, prevent occupied ✓
- **✅ Reatribuição**: Release + reassign flow ✓

### Próximos Passos (Sprint 2+)
- HTTP views ainda precisam de serializers explícitos
- Adicionar validation layer (pydantic/marshmallow)
- Integration com outros módulos (restaurantes, clientes, pagamentos)
- Adicionar API documentation (OpenAPI/Swagger)

---

## 🚀 Rodando Localmente

### Pré-requisitos
```bash
cd service/backend
pip install -r requirements.txt
python3 manage.py migrate
```

### Rodando Testes BDD
```bash
# Inicia Docker Compose (PostgreSQL + Django)
docker-compose up -d

# Rode os testes
python3 -m pytest tests/steps/test_deliverers_steps.py -v
```

### Rodando Django Dev Server
```bash
python3 manage.py runserver 0.0.0.0:8000
```

### Exemplo de Request (cURL)
```bash
# Register deliverer
curl -X POST http://localhost:8000/api/deliverers/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Ana","phone":"11999999999","region":"Zona Sul"}'

# List by status
curl http://localhost:8000/api/deliverers/?status=AVAILABLE

# Assign order
curl -X POST http://localhost:8000/api/orders/assign/ \
  -H "Content-Type: application/json" \
  -d '{"order_id":"uuid","region":"Zona Sul"}'
```

---

## 📝 Notas Técnicas

### Decisões de Design
1. **Dataclass entities** ao invés de modelos ORM puros
   - Separa domain logic de DB persistence
   - Tipagem forte sem overhead

2. **Repository pattern via ports**
   - Facilita testes (mock repositories)
   - Permite trocar DB no futuro sem impacto

3. **Síncrono sem eventos**
   - MVP não precisa de complexidade
   - Fácil evolução depois (pub/sub, queues)

4. **PostgreSQL direto sem cache**
   - Sprint 1 focado em funcionalidade
   - Redis adiciona depois se houver latência

### Trade-offs
- **Menos abstração** = mais rápido entregar, menos teste de mocks
- **Sem schema validation** = BDD cobre happy paths, precisa adicionar marshmallow depois
- **HTTP parsing manual** = simples agora, serializers depois

---

## 🎯 Sumário

A implementação de Deliverers Sprint 1 entrega:
- ✅ 4 camadas bem definidas (Domain → Service → Repository → Model)
- ✅ 8 cenários BDD testando fluxo completo
- ✅ 5 commits lógicos e rastreáveis
- ✅ 0 complexidade desnecessária
- ✅ Pronto para evoluir em Sprint 2/3/4

Próxima etapa: Mergear PR e validar integração com outros módulos (restaurantes, clientes, pagamentos) que também rodamo em paralelo.
