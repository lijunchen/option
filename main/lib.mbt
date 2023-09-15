pub enum Option[T] {
  None
  Some(T)
}

pub func is_none[T](x: Option[T]) -> Bool {
  match x {
    None => true
    Some(_) => false
  }
}

pub func is_some[T](x: Option[T]) -> Bool {
  match x {
    None => false
    Some(_) => true
  }
}
