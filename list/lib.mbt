pub func length[T](self: List[T]) -> Int {
  match self {
    Nil => 0
    Cons(_, rest) => 1 + length(rest)
  }
}

pub func is_empty[T](self: List[T]) -> Bool {
  match self {
    Nil => true
    _ => false
  }
}

pub func cons[T](self: List[T], elem: T) -> List[T] {
  Cons(elem, self)
}

pub func hd[T](self: List[T]) -> T {
  match self {
    Nil => abort("empty list")
    Cons(head, _) => head
  }
}

pub func contains[T: Eq](self: List[T], target: T) -> Bool {
  match self {
    Nil => false
    Cons(head, tail) => if head == target { true } else { tail.contains(target) }
  }
}

pub func map[T, U](self: List[T], f: (T) -> U) -> List[U] {
  match self {
    Nil => Nil
    Cons(head, tail) => Cons(f(head), tail.map(f))
  }
}

pub func mapi[T, U](self: List[T], f: (Int, T) -> U) -> List[U] {
  fn go(i: Int, f: (Int, T) -> U, xs: List[T]) -> List[U] {
    match xs {
      Nil => Nil
      Cons(head, tail) => Cons(f(i, head), go(i + 1, f, tail))
    }
  }

  go(0, f, self)
}

pub func filter[T](self: List[T], p: (T) -> Bool) -> List[T] {
  match self {
    Nil => Nil
    Cons(head, tail) => if p(head) { Cons(head, tail.filter(p)) } else { tail.filter(p) }
  }
}

pub func fold_left[T, U](self: List[T], f: (U, T) -> U, init: U) -> U {
  match self {
    Nil => init
    Cons(head, tail) => tail.fold_left(f, f(init, head))
  }
}

pub func fold_right[T, U](self: List[T], f: (T, U) -> U, init: U) -> U {
  match self {
    Nil => init
    Cons(head, tail) => f(head, tail.fold_right(f, init))
  }
}

pub func assoc[K: Eq, V](xs: List[(K, V)], key: K) -> Option[V] {
  match xs {
    Nil => None
    Cons((k, v), tail) => if k == key { Some(v) } else { assoc(tail, key) }
  }
}