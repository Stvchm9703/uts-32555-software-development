```mermaid 
classDiagram
  class BaseModel {
    created_at : DatetimeField
    id : IntField
    updated_at : DatetimeField
  }
  class DummyModel {
    id : IntField
    name : CharField
  }
  class OrderModel {
    id : IntField
    items : CharField
    name : CharField
  }

```