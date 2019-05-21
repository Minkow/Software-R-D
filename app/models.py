from app import db
from flask_login import UserMixin
from flask_restful import Api, Resource
import hashlib
import json
from datetime import datetime
import uuid
from flask import request
from py2neo import Graph, NodeSelector, Node, Relationship
from py2neo.ogm import GraphObject, Property
from app import app

api = Api(app)

class glovar():
    editsnode = ''
    editenode = ''
    editrelation = ''
#pass paras to input.value showed on editrel.html

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
 #   name = db.Column(db.String(256))
    username = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256))
    role = db.Column(db.Enum('Manager', 'User'))

    def check_password(self, password):
        s = hashlib.md5()
        s.update(password.encode('utf-8'))
        print(s.hexdigest())
        return self.password == s.hexdigest()


class Search(Graph, NodeSelector, Node, Relationship):
    def getnode(graph, text): #input name
        cql = "MATCH (n{name:'" + text + "'}) return n"
        res = graph.run(cql).data()
        #print(res)
        if(res):
            node = res[0].get('n')
        else:
            node = []
        return node

    def getrel(graph, s, r, e):
        if(graph.match_one(start_node=s, rel_type=r, end_node=e, bidirectional=True) != None):
            relation =graph.match(start_node=s, rel_type=r, end_node=e, bidirectional=True)
            return relation
        else:
            return None

    def getrelation(graph, node):
        relations = graph.match(start_node=node, bidirectional=True)
        link1 = []
        link2 = []
        page1 = []
        page2 = []
        for i in relations:
            print(i)
            type = i.type()
            snode = i.start_node()
            enode = i.end_node()
            print(snode)
            print(enode)
            sname = snode['name']
            ename = enode['name']


            if (snode == node):
                if(type == 'type'):
                    link1.append(type + ": ")
                    page1.append(ename)
                else:
                    link1.append(type + ": ")
                    page1.append(ename)
            else:
                link2.append("->" + type + ":" + ename)
                page2.append(sname)
        if(link1 != [] and link2 != []):
            t1 = list(zip(link1, page1))
            t1.sort()
            link1[:], page1[:] = zip(*t1)
        if(link2 != [] and link2 != []):
            t2 = list(zip(page2, link2))
            t2.sort()
            page2[:], link2[:] = zip(*t2)
        link = link1 + link2
        page = page1 + page2
        leng = len(link1)

        return link, page, leng

    def getoutnode(graph, node):
        data = []
        rel = []
        edge = []
        if(graph.match_one(start_node=node, bidirectional=False)!=None):
            r = graph.match(start_node=node, bidirectional=False)
            for i in r:
                sid = hash(i.start_node())
                eid = hash(i.end_node())
                type = i.type()
                edge = edge + [{"data": {'source': sid, 'target': eid, 'relationship': type}}]
                data.append(i.end_node())
                rel.append('out')
        return data,rel,edge

    def getinnode(graph, node):
        data = []
        edge = []
        if(graph.match_one(end_node=node, bidirectional=False)!=None):
            rel = graph.match(end_node=node, bidirectional=False)
            for i in rel:
                sid = hash(i.start_node())
                eid = hash(i.end_node())
                type = i.type()
                edge = edge + [{"data": {'source': sid, 'target': eid, 'relationship': type}}]
                data.append(i.start_node())
        return data,edge

    def buildnode(node, type):
        name = node['name']
        id = hash(node)
        data={'id':id,'name':name,'type':type}
        return {"data": data}

    def nodesearch(graph, nodename):
        n = Search.getnode(graph, nodename)
        outrelations = graph.match(start_node=n, bidirectional=False)
        outnodes = {}
        for i in outrelations:
            outnodes[i.end_node()['name']] = i.type()
        inrelations = graph.match(end_node=n, bidirectional=False)
        innodes = {}
        for i in inrelations:
            innodes[i.start_node()['name']] = i.type()
        return json.dumps({'type': n['Nodetype'], 'out': outnodes, 'in': innodes}, ensure_ascii=False)


class Edit(Graph, NodeSelector, Node, Relationship):

    def nodeadd(graph, node, type):
        graph.create(Node("Ontology",name = node,Nodetype = type))

    def nodeedit(graph, node1, node2, type2):
        n = Search.getnode(graph, node1)
        if n!=[]:
            n['name'] = node2
            n['Nodetype'] = type2
            graph.update(n)
            return True
        else:
            return False


    def relationadd(graph, startnode, relation, endnode):
        if Search.getnode(graph,startnode) == []:
            return False
        else:
            startnode = Search.getnode(graph,startnode)
        #print(startnode)
        if Search.getnode(graph,endnode) == []:
            return False
        else:
            endnode = Search.getnode(graph, endnode)
        #print(endnode)
        rel = Relationship(startnode, relation, endnode)
        #print(rel)
        s = startnode | endnode | rel
        graph.create(s)
        return True

    def relationdelete(graph, sname, rel, ename):
        if Search.getnode(graph, sname) == []:
            return False
        else:
            startnode = Search.getnode(graph, sname)
        if Search.getnode(graph, ename) == []:
            return False
        else:
            endnode = Search.getnode(graph, ename)
        # print(endnode)
        rel = Relationship(startnode, rel, endnode)
        # print(rel)
        s = startnode | endnode | rel
        graph.delete(s)
        return True

    def nodedelete(graph, node):
        n = Search.getnode(graph, node)
        if n != []:
            graph.delete(n)
            return ('Success')
        else:
            return ('False')

    def relationedit(graph, fromstart, fromrel, fromend, tostart, torel, toend):
        if Search.getnode(graph, fromstart) == []:
            return False
        else:
            fstart = Search.getnode(graph, fromstart)
        if Search.getnode(graph, fromend) == []:
            return False
        else:
            fend = Search.getnode(graph, fromend)
        if Search.getnode(graph, tostart) == []:
            return False
        else:
            tstart = Search.getnode(graph, tostart)
        if Search.getnode(graph, toend) == []:
            return False
        else:
            tend = Search.getnode(graph, toend)
        tri = Search.getrel(graph, fstart, fromrel, fromend)
        if tri!=None:
            graph.delete(tri)
            Edit.relationadd(graph, tostart, torel, toend)
            return True
        else:
            return False





# api.add_resource(NodeSearch, '/nodesearch')



