userdata = """#cloud-config
hostname: "coreos"
  units:
    - name: "cbweb.service"
      command: "start"
      content: |
        [Unit]
        Description=CBWeb
        Author=Ken Erwin
        After=docker.service

        [Service]
        Restart=always
        ExecStart=/usr/bin/docker run -d -p 80:80 --name cbweb kenerwin88/cbweb
        ExecStop=/usr/bin/docker stop -t 2 cbweb
ssh_authorized_keys:
  - "pubkey
"""
contents = open('sample_public_key.pem').read()
userdata = userdata.replace('pubkey', contents)[:-2] + '"'
print userdata
