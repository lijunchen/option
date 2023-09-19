pub func hash(self: String) -> Int {
  var h = 7
  var i = 0
  while i < self.length() {
    h = h * 31 + self.get(i).to_int()
    i = i + 1
  }
  h
}

pub func hash(self: Bool) -> Int {
  if self { 1 } else {0}
}

pub func hash(self: Float64) -> Int {
  self.to_int().hash()
}

pub func hash(self: Char) -> Int {
  self.to_int()
}

pub func hash(self: Int64) -> Int {
  let lo = self.to_int();
  lo.hash()
}

pub func hash(self: Int) -> Int {
  var x = self.lsr(16).lxor(self) * 0x45d9f3b;
  x = x.lsr(16).lxor(x) * 0x45d9f3b;
  x = x.lsr(16).lxor(x);
  x
}
