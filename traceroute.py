import argparse
import subprocess
import re

def traceroute(target, progressive=False, output_file=None):
    # Commande traceroute adaptée à Windows
    command = ["tracert", target]
    
    if progressive:
        # Utilisation de subprocess.Popen pour un affichage progressif
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
            with open(output_file, 'w') if output_file else None as file:
                for line in process.stdout:
                    ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', line)
                    if ip_match:
                        ip = ip_match.group(0)
                        print(ip)
                        if file:
                            file.write(ip + '\n')
    else:
        # Utilisation de subprocess.run pour un affichage après exécution complète
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        ips = re.findall(r'\d+\.\d+\.\d+\.\d+', result.stdout)
        for ip in ips:
            print(ip)
        if output_file:
            with open(output_file, 'w') as file:
                file.write('\n'.join(ips) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Traceroute script")
    parser.add_argument("target", help="URL or IP address to traceroute")
    parser.add_argument("-p", "--progressive", action="store_true", help="Display results progressively")
    parser.add_argument("-o", "--output-file", help="Output file to save the results")
    
    args = parser.parse_args()
    traceroute(args.target, args.progressive, args.output_file)
