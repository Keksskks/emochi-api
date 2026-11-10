# 03_browse_all_ai.py
from emochi import Emochi

client = Emochi()

print("Dang tai tat ca nhan vat AI tu he thong Emochi...")
all_chars = client.get_all_characters(max_total=50)

print(f"\nTong hop thanh cong {len(all_chars)} nhan vat AI doc nhat:")
for i, c in enumerate(all_chars, 1):
    desc = (c.description[:60] + "...") if len(c.description) > 60 else c.description
    print(f"[{i:2d}] {c.name} ({c.category})")
    print(f"     ID: {c.id}")
    print(f"     Avatar: {c.avatar_url}")
    print(f"     Mo ta: {desc}")
    print("-" * 50)

print("\nDang tai nhan vat phan theo 12 the loai:")
by_tags = client.get_characters_by_tags(take=5)
for tag, chars in by_tags.items():
    print(f"\nThe loai: {tag.upper()} ({len(chars)} nhan vat)")
    for c in chars[:2]:
        print(f"  * {c.name} -> {c.avatar_url}")
