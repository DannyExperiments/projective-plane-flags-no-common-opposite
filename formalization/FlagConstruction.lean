import Std

/- Two distinct points determine a unique line, and every pair of lines
has a common point. These axioms suffice for the no-opposite conclusion. -/
namespace FlagConstruction

structure Plane (Point Line : Type) where
  onLine : Point → Line → Prop
  join : Point → Point → Line
  leftOn : ∀ a b, a ≠ b → onLine a (join a b)
  rightOn : ∀ a b, a ≠ b → onLine b (join a b)
  uniqueLine : ∀ {a b l n}, a ≠ b → onLine a l → onLine b l →
    onLine a n → onLine b n → l = n
  commonPoint : ∀ l n, ∃ x, onLine x l ∧ onLine x n

variable {Point Line : Type} (P : Plane Point Line)

/-- The selected flags (A,m), (B,BA), and (X,BX) for X on m other than R,A. -/
def Selected (m : Line) (R A B x : Point) (l : Line) : Prop :=
  (x = A ∧ l = m) ∨ (x = B ∧ l = P.join B A) ∨
    (P.onLine x m ∧ x ≠ R ∧ x ≠ A ∧ l = P.join B x)

def Opposite (x : Point) (l : Line) (y : Point) (n : Line) : Prop :=
  ¬ P.onLine y l ∧ ¬ P.onLine x n

theorem selected_incident {m : Line} {R A B x : Point} {l : Line}
    (ha : P.onLine A m) (hb : ¬ P.onLine B m) (sel : Selected P m R A B x l) :
    P.onLine x l := by
  rcases sel with ⟨rfl,rfl⟩ | ⟨rfl,rfl⟩ | ⟨hx,_,_,rfl⟩
  · exact ha
  · exact P.leftOn _ _ (fun eq => hb (eq ▸ ha))
  · exact P.rightOn _ _ (fun eq => hb (eq ▸ hx))

/-- Every point of m except R occurs as a selected point. -/
theorem selected_point {m : Line} {R A B x : Point}
    (hx : P.onLine x m) (hxr : x ≠ R) : ∃ l, Selected P m R A B x l := by
  by_cases h : x = A
  · exact ⟨m, Or.inl ⟨h,rfl⟩⟩
  · exact ⟨P.join B x, Or.inr (Or.inr ⟨hx,hxr,h,rfl⟩)⟩

/-- Joining B to any point of m except R gives a selected line. -/
theorem selected_join {m : Line} {R A B x : Point}
    (hx : P.onLine x m) (hxr : x ≠ R) : ∃ p, Selected P m R A B p (P.join B x) := by
  by_cases h : x = A
  · subst x; exact ⟨B, Or.inr (Or.inl ⟨rfl,rfl⟩)⟩
  · exact ⟨x, Or.inr (Or.inr ⟨hx,hxr,h,rfl⟩)⟩

/-- The selected family has no common opposite, with no bound on plane order. -/
theorem no_common_opposite {m : Line} {R A B y : Point} {n : Line}
    (hr : P.onLine R m)
    (hb : ¬ P.onLine B m) (hyn : P.onLine y n) :
    ¬ (∀ x l, Selected P m R A B x l → Opposite P x l y n) := by
  intro opp
  have hym := (opp A m (Or.inl ⟨rfl,rfl⟩)).1
  have selB : Selected P m R A B B (P.join B A) := Or.inr (Or.inl ⟨rfl,rfl⟩)
  have hbn := (opp B _ selB).2
  have byne : B ≠ y := fun h => hbn (h ▸ hyn)
  have bj := P.leftOn B y byne
  have yj := P.rightOn B y byne
  obtain ⟨v,hvm,hvj⟩ := P.commonPoint m (P.join B y)
  have vR : v = R := by
    apply Classical.byContradiction
    intro h
    have bv : B ≠ v := fun e => hb (e ▸ hvm)
    have lines := P.uniqueLine bv bj hvj (P.leftOn B v bv) (P.rightOn B v bv)
    obtain ⟨p,hp⟩ := selected_join P (A := A) (B := B) hvm h
    exact (opp p _ hp).1 (lines ▸ yj)
  subst v
  obtain ⟨x,hxm,hxn⟩ := P.commonPoint m n
  by_cases xr : x = R
  · subst x
    have yr : y ≠ R := fun h => hym (h ▸ hr)
    have lines := P.uniqueLine yr yj hvj hyn hxn
    exact hbn (lines ▸ bj)
  · obtain ⟨l,hl⟩ := selected_point P (A := A) (B := B) hxm xr
    exact (opp x l hl).2 hxn

/-- A third point X on m gives the two nondegeneracy conditions. -/
theorem neither_line_nor_pencil {m : Line} {R A B X : Point}
    (ha : P.onLine A m) (hx : P.onLine X m) (hxr : X ≠ R) (hxa : X ≠ A)
    (hb : ¬ P.onLine B m) :
    (¬ ∃ n, ∀ p l, Selected P m R A B p l → P.onLine p n) ∧
    (¬ ∃ y, ∀ p l, Selected P m R A B p l → P.onLine y l) := by
  have sA : Selected P m R A B A m := Or.inl ⟨rfl,rfl⟩
  have sB : Selected P m R A B B (P.join B A) := Or.inr (Or.inl ⟨rfl,rfl⟩)
  have sX : Selected P m R A B X (P.join B X) := Or.inr (Or.inr ⟨hx,hxr,hxa,rfl⟩)
  constructor
  · rintro ⟨n,h⟩
    have nm := P.uniqueLine hxa (h _ _ sX) (h _ _ sA) hx ha
    exact hb (nm ▸ h _ _ sB)
  · rintro ⟨y,h⟩
    have byne : B ≠ y := fun e => hb (e ▸ h _ _ sA)
    have ba : B ≠ A := fun e => hb (e ▸ ha)
    have bx : B ≠ X := fun e => hb (e ▸ hx)
    have jj := P.uniqueLine byne (P.leftOn _ _ ba) (h _ _ sB)
      (P.leftOn _ _ bx) (h _ _ sX)
    have ax : P.onLine A (P.join B X) := jj ▸ P.rightOn _ _ ba
    have jm := P.uniqueLine hxa (P.rightOn _ _ bx) ax hx ha
    exact hb (jm ▸ P.leftOn _ _ bx)

end FlagConstruction
#print axioms FlagConstruction.selected_incident
#print axioms FlagConstruction.no_common_opposite
#print axioms FlagConstruction.neither_line_nor_pencil
