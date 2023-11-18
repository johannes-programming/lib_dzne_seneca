
import xml.dom.minidom


def get_cline(prog, *, query, out, db):
    return [
        prog,
        '-db', db,
        '-task', 'blastn',
        '-dust', 'no',
        '-outfmt', '5',
        '-max_target_seqs', '1',
        '-evalue', '0.0001',
        '-sorthits', '1',
        '-query', query, 
        '-out', out,
    ]

def parse(text):
    data = xml.dom.minidom.parseString(text)
    store = dict()
    store['query-id'] = _get(data, "BlastOutput", "BlastOutput_iterations", "Iteration", "Iteration_query-def")
    store['subject-id'] = _get(data, "BlastOutput", "BlastOutput_iterations", "Iteration", "Iteration_hits", "Hit", "Hit_id")
    store['bit-score'] = float(_get(data, "BlastOutput", "BlastOutput_iterations", "Iteration", "Iteration_hits", "Hit", "Hsp", "Hsp_bit-score"))
    store['evalue'] = float(_get(data, "BlastOutput", "BlastOutput_iterations", "Iteration", "Iteration_hits", "Hit", "Hsp", "Hsp_evalue"))
    return store

def _get(data, *keys, kind=str):
    if data is None:
        return None
    ans = data
    try:
        for key in keys:
            ans = ans.getElementsByTagName(key)[0]
        ans = ans.childNodes[0]
    except ValueError:
        return float('nan')
    except IndexError:
        return float('nan')
    ans = ans.nodeValue
    if type(ans) is not str:
        raise TypeError()
    return ans



            





