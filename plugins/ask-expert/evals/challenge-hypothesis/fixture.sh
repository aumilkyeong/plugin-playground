#!/usr/bin/env bash
# 상품 목록과 상세 화면이 있는 작은 Next.js 앱을 만든다. 목록의 필터와 정렬은 useState에만 있다.
set -euo pipefail

cat > package.json <<'JSON'
{
  "name": "shop-web",
  "private": true,
  "scripts": { "dev": "next dev", "build": "next build", "test": "vitest" },
  "dependencies": { "next": "15.1.0", "react": "19.0.0", "react-dom": "19.0.0" },
  "devDependencies": { "typescript": "5.6.3", "vitest": "2.1.8" }
}
JSON

mkdir -p app/products/'[id]' lib
cat > lib/api.ts <<'TS'
export type Product = { id: string; name: string; category: string; price: number };

export async function fetchProducts(params: { category?: string; sort?: "price" | "new" }) {
  const query = new URLSearchParams(params as Record<string, string>);
  const res = await fetch(`/api/products?${query}`);
  return (await res.json()) as Product[];
}
TS

cat > app/products/page.tsx <<'TSX'
"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { fetchProducts, type Product } from "@/lib/api";

export default function ProductsPage() {
  const [category, setCategory] = useState("all");
  const [sort, setSort] = useState<"price" | "new">("new");
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    fetchProducts({ category: category === "all" ? undefined : category, sort }).then(setProducts);
  }, [category, sort]);

  return (
    <main>
      <select value={category} onChange={(e) => setCategory(e.target.value)}>
        <option value="all">전체</option>
        <option value="shoes">신발</option>
        <option value="bags">가방</option>
      </select>
      <select value={sort} onChange={(e) => setSort(e.target.value as "price" | "new")}>
        <option value="new">최신순</option>
        <option value="price">가격순</option>
      </select>
      <ul>
        {products.map((p) => (
          <li key={p.id}>
            <Link href={`/products/${p.id}`}>{p.name}</Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
TSX

cat > 'app/products/[id]/page.tsx' <<'TSX'
import Link from "next/link";

export default async function ProductDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const product = await fetch(`${process.env.API_ORIGIN}/products/${id}`).then((r) => r.json());
  return (
    <main>
      <Link href="/products">목록으로</Link>
      <h1>{product.name}</h1>
      <p>{product.price}원</p>
    </main>
  );
}
TSX
