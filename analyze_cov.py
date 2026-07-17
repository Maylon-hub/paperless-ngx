import xml.etree.ElementTree as ET
import sys

def analyze_coverage():
    tree = ET.parse('coverage.xml')
    root = tree.getroot()
    
    files = []
    
    for cls in root.iter('class'):
        filename = cls.get('filename')
        line_rate = float(cls.get('line-rate'))
        lines_valid = int(cls.get('complexity', 0)) # Actually let's count the lines
        
        lines = cls.find('lines')
        if lines is None:
            continue
            
        valid_lines = len(lines.findall('line'))
        if valid_lines == 0:
            continue
            
        hits = sum(1 for line in lines.findall('line') if int(line.get('hits')) > 0)
        coverage = hits / valid_lines if valid_lines > 0 else 1.0
        
        files.append((filename, coverage, valid_lines, valid_lines - hits))
        
    # Sort by coverage ascending, then by number of missing lines descending
    files.sort(key=lambda x: (x[1], -x[3]))
    
    print("Files with lowest coverage:")
    for f in files[:30]:
        print(f"{f[0]:<50} | Coverage: {f[1]*100:>6.2f}% | Missing lines: {f[3]:>4} / {f[2]:>4}")

if __name__ == '__main__':
    analyze_coverage()
