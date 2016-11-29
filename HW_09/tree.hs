module Tree where

import Prelude hiding (lookup)

data BinaryTree k v = Null | Node { key		:: k
                                  ,	val	    :: v
                                  ,	l		:: BinaryTree k v
                                  ,	r		:: BinaryTree k v
                                  }

lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup k Null = Nothing
lookup k t = if k == (key t)
	         then Just (val t)
	         else if k < (key t)
		          then (lookup k (l t))
		          else (lookup k (r t))

merge :: BinaryTree k v -> BinaryTree k v -> BinaryTree k v
merge Null b = b
merge a Null = a
merge a b = Node (key b) (val b) (merge a (l b)) (r b)

insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert k v Null = Node k v Null Null
insert k v t = if k == (key t)
	           then Node k v (l t) (r t)
	           else if k < (key t)
		            then Node (key t) (val t) (insert k v (l t)) (r t)
		            else Node (key t) (val t) (l t) (insert k v (r t))

delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete k Null = Null
delete k t = if k == (key t)
	         then merge (l t) (r t)
	         else if k < (key t)
		          then Node (key t) (val t) (delete k (l t)) (r t)
		          else Node (key t) (val t) (l t) (delete k (r t))
