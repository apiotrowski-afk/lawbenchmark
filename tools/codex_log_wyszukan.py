"""Wyciąg wywołań wyszukiwania z wyjścia `codex exec --json` (zalecenie z artykułu v1.2, 2026-10-25: zapisywać
każde wywołanie narzędzia sędziego — zapytanie i źródło — żeby dało się sprawdzić, co sędzia faktycznie sprawdził).
Format zdarzeń Codex bywa różny między wersjami, więc wyciąg jest defensywny: z każdego zdarzenia, które dotyczy
web_search, zbiera pola wyglądające na zapytanie albo adres. Nic nie zgaduje — brak pól = pusty wpis.

Uwaga (1.0.3): licznik „wyszukan” liczy każde zdarzenie z web_search w logu Codex CLI, a log zapisuje start i koniec
każdej akcji oraz otwarcia stron. W danych i raporcie od 1.0.3 wartości Codex są dzielone przez 2 i podawane jako
„web actions” (wyszukania + otwarcia stron), zob. CHANGELOG."""
import json

_KLUCZE_ZAPYTANIE = ("query", "q", "search_query", "queries")
_KLUCZE_ADRES = ("url", "uri", "link", "source_url")


def _zbierz(o, klucze, out):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in klucze:
                if isinstance(v, str) and v.strip():
                    out.append(v.strip())
                elif isinstance(v, list):
                    out.extend(x.strip() for x in v if isinstance(x, str) and x.strip())
            else:
                _zbierz(v, klucze, out)
    elif isinstance(o, list):
        for x in o:
            _zbierz(x, klucze, out)


def wyszukania(stdout: str, limit: int = 30) -> dict:
    """Zwraca {"wyszukan": liczba zdarzeń web_search, "zapytania": [...], "zrodla_sedziego": [...]}."""
    licznik, zap, adr = 0, [], []
    for linia in stdout.splitlines():
        if '"web_search"' not in linia:
            continue
        licznik += 1
        try:
            zd = json.loads(linia)
        except ValueError:
            continue
        _zbierz(zd, _KLUCZE_ZAPYTANIE, zap)
        _zbierz(zd, _KLUCZE_ADRES, adr)
    uniq = lambda xs: list(dict.fromkeys(xs))
    return {"wyszukan": licznik, "zapytania": uniq(zap)[:limit], "zrodla_sedziego": uniq(adr)[:limit]}
