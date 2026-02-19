#!/usr/bin/env python3
"""
Скрипт для извлечения доменов первого уровня (apex domains) из списков доменов.
Обрабатывает все txt-файлы в папке platforms и сохраняет результаты в отдельную папку.
"""

import os
from pathlib import Path


def extract_apex_domain(domain):
    """
    Извлекает домен первого уровня (apex domain) из полного доменного имени.
    
    Примеры:
        subdomain.example.com -> example.com
        www.example.co.uk -> example.co.uk
        example.com -> example.com
    
    Использует простую эвристику для общих суффиксов.
    """
    domain = domain.strip().lower()
    
    # Убираем точку в конце, если она есть
    if domain.endswith('.'):
        domain = domain[:-1]
    
    if not domain:
        return None
    
    parts = domain.split('.')
    
    # Если домен состоит из 1 части, возвращаем как есть
    if len(parts) <= 1:
        return domain
    
    # Список двухуровневых TLD (неполный, для более точной работы используйте Public Suffix List)
    two_level_tlds = {
        'co.uk', 'co.jp', 'co.kr', 'co.nz', 'co.za', 'co.il', 'co.in',
        'com.au', 'com.br', 'com.cn', 'com.mx', 'com.ar', 'com.tr',
        'org.uk', 'org.au', 'ac.uk', 'gov.uk', 'net.au'
    }
    
    # Проверяем последние две части на совпадение с двухуровневым TLD
    if len(parts) >= 3:
        potential_tld = f"{parts[-2]}.{parts[-1]}"
        if potential_tld in two_level_tlds:
            # Берём домен + двухуровневый TLD
            return '.'.join(parts[-3:]) if len(parts) >= 3 else domain
    
    # Стандартный случай: берём последние две части (домен + TLD)
    return '.'.join(parts[-2:])


def process_file(input_path, output_path):
    """
    Обрабатывает один файл: читает домены, извлекает apex-домены, 
    удаляет дубликаты и сохраняет результат.
    """
    apex_domains = set()
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # Пропускаем пустые строки и комментарии
                if not line or line.startswith('#'):
                    continue
                
                # Извлекаем домен (на случай, если в строке есть что-то ещё)
                domain = line.split()[0] if line.split() else line
                
                apex = extract_apex_domain(domain)
                if apex:
                    apex_domains.add(apex)
        
        # Сохраняем результат
        with open(output_path, 'w', encoding='utf-8') as f:
            for domain in sorted(apex_domains):
                f.write(f"{domain}\n")
        
        return len(apex_domains)
    
    except Exception as e:
        print(f"Ошибка при обработке {input_path}: {e}")
        return 0


def main():
    # Определяем пути
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    platforms_dir = project_dir / 'platforms'
    output_dir = project_dir / 'platforms_apex'
    
    # Создаём выходную папку, если её нет
    output_dir.mkdir(exist_ok=True)
    
    # Находим все txt-файлы в папке platforms
    txt_files = list(platforms_dir.glob('*.txt'))
    
    if not txt_files:
        print(f"В папке {platforms_dir} не найдено txt-файлов")
        return
    
    print(f"Найдено {len(txt_files)} txt-файлов для обработки")
    print(f"Результаты будут сохранены в: {output_dir}\n")
    
    total_processed = 0
    
    # Обрабатываем каждый файл
    for input_file in sorted(txt_files):
        output_file = output_dir / input_file.name
        
        count = process_file(input_file, output_file)
        total_processed += 1
        
        print(f"✓ {input_file.name}: {count} уникальных apex-доменов")
    
    print(f"\nГотово! Обработано {total_processed} файлов")
    print(f"Результаты сохранены в папке: {output_dir}")


if __name__ == '__main__':
    main()
